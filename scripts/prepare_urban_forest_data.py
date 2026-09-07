import csv
import json
import math
import re
import time
from copy import deepcopy
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"

DATASETS = {
    "heritage_trees": {
        "id": "d_644ff187b6d14d6316f47284a4a6c81f",
        "title": "Heritage Trees",
        "agency": "NParks",
    },
    "subzone_boundary": {
        "id": "d_8594ae9ff96d0c708bc2af633048edfb",
        "title": "Master Plan 2019 Subzone Boundary (No Sea)",
        "agency": "URA",
    },
    "parks_nature_reserves": {
        "id": "d_77d7ec97be83d44f61b85454f844382f",
        "title": "NParks Parks and Nature Reserves",
        "agency": "NParks",
    },
    "tree_conservation_areas": {
        "id": "d_52b9eabe398353bd6acd9aee15b13f72",
        "title": "Tree Conservation Area",
        "agency": "NParks",
    },
    "hdb_existing_buildings": {
        "id": "d_16b157c52ed637edd6ba1232e026258d",
        "title": "HDB Existing Building",
        "agency": "HDB",
    },
}


def ensure_dirs():
    for path in (RAW_DIR, PROCESSED_DIR, DOCS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def poll_download_url(dataset_id):
    url = f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"
    response = None
    for attempt in range(6):
        response = requests.get(url, timeout=60)
        if response.status_code != 429:
            response.raise_for_status()
            break
        wait_seconds = 10 * (attempt + 1)
        print(f"Rate limited by data.gov.sg for {dataset_id}; waiting {wait_seconds}s")
        time.sleep(wait_seconds)
    else:
        response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 0:
        raise RuntimeError(f"{dataset_id}: {payload.get('errMsg')}")
    return payload["data"]["url"]


def download_dataset(key, meta):
    out_path = RAW_DIR / f"{key}.geojson"
    url_path = RAW_DIR / f"{key}.download_url.txt"
    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path
    download_url = poll_download_url(meta["id"])
    time.sleep(3)
    data = requests.get(download_url, timeout=180)
    data.raise_for_status()
    out_path.write_bytes(data.content)
    url_path.write_text(download_url, encoding="utf-8")
    return out_path


def load_geojson(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_geojson(obj, path):
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def valid_lonlat(coords):
    if not isinstance(coords, list) or len(coords) < 2:
        return False
    lon, lat = coords[:2]
    if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
        return False
    return 103.55 <= lon <= 104.15 and 1.15 <= lat <= 1.55


def iter_rings(geometry):
    if not geometry:
        return
    gtype = geometry.get("type")
    coords = geometry.get("coordinates", [])
    if gtype == "Polygon":
        for ring in coords:
            yield ring
    elif gtype == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                yield ring


def outer_rings(geometry):
    if not geometry:
        return []
    if geometry.get("type") == "Polygon":
        return geometry.get("coordinates", [])[:1]
    if geometry.get("type") == "MultiPolygon":
        return [poly[0] for poly in geometry.get("coordinates", []) if poly]
    return []


def clean_feature_collection(fc, keep_geometry_types=None):
    features = []
    for feature in fc.get("features", []):
        geom = feature.get("geometry")
        if not geom or not geom.get("coordinates"):
            continue
        if keep_geometry_types and geom.get("type") not in keep_geometry_types:
            continue
        if geom.get("type") == "Point" and not valid_lonlat(geom.get("coordinates", [])):
            continue
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}


def parse_heritage_description(description):
    description = description or ""
    common_name = ""
    location = ""
    match = re.search(r"Common Name\s*:\s*(.*?)\.\s*Found in\s*(.*)", description, flags=re.I | re.S)
    if match:
        common_name = match.group(1).strip()
        location = match.group(2).strip()
    else:
        common = re.search(r"Common Name\s*:\s*(.*?)(?:\.|$)", description, flags=re.I | re.S)
        found = re.search(r"Found in\s*(.*)", description, flags=re.I | re.S)
        if common:
            common_name = common.group(1).strip()
        if found:
            location = found.group(1).strip()
    if common_name in {".", "-", "NA"}:
        common_name = ""
    return common_name, location


def clean_heritage_trees(fc):
    seen = set()
    features = []
    for feature in clean_feature_collection(fc, {"Point"}).get("features", []):
        props = feature.get("properties", {})
        coords = feature["geometry"]["coordinates"]
        heritage_id = str(props.get("HT") or "").strip()
        dedupe_key = heritage_id or (round(coords[0], 7), round(coords[1], 7), props.get("NAME"))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        common_name, location = parse_heritage_description(props.get("DESCRIPTION"))
        new_props = {
            "heritage_id": heritage_id,
            "common_name": common_name,
            "scientific_name": str(props.get("NAME") or "").strip(),
            "location_description": location,
            "hyperlink": str(props.get("HYPERLINK") or "").strip(),
            "source_objectid": props.get("OBJECTID"),
            "source_updated": str(props.get("FMEL_UPD_D") or "").strip(),
            "point_source": "NParks Heritage Trees",
            "proxy_note": "Official heritage tree point; not a complete all-trees/street-trees inventory.",
        }
        features.append({"type": "Feature", "geometry": feature["geometry"], "properties": new_props})
    return {"type": "FeatureCollection", "features": features}


def bbox_for_geometry(geometry):
    xs, ys = [], []
    for ring in iter_rings(geometry):
        for coord in ring:
            if len(coord) >= 2:
                xs.append(coord[0])
                ys.append(coord[1])
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def point_in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    if n < 3:
        return False
    x1, y1 = ring[0][:2]
    for i in range(1, n + 1):
        x2, y2 = ring[i % n][:2]
        if ((y1 > lat) != (y2 > lat)) and (lon < (x2 - x1) * (lat - y1) / ((y2 - y1) or 1e-12) + x1):
            inside = not inside
        x1, y1 = x2, y2
    return inside


def point_in_polygon_geometry(lon, lat, geometry):
    bbox = geometry.get("_bbox")
    if bbox and not (bbox[0] <= lon <= bbox[2] and bbox[1] <= lat <= bbox[3]):
        return False
    gtype = geometry.get("type")
    coords = geometry.get("coordinates", [])
    polygons = [coords] if gtype == "Polygon" else coords if gtype == "MultiPolygon" else []
    for polygon in polygons:
        if not polygon or not point_in_ring(lon, lat, polygon[0]):
            continue
        if any(point_in_ring(lon, lat, hole) for hole in polygon[1:]):
            continue
        return True
    return False


def ring_area_sq_m(ring):
    if len(ring) < 3:
        return 0.0
    lat0 = math.radians(sum(pt[1] for pt in ring) / len(ring))
    meters_per_deg_lat = 111_320.0
    meters_per_deg_lon = 111_320.0 * math.cos(lat0)
    pts = [(pt[0] * meters_per_deg_lon, pt[1] * meters_per_deg_lat) for pt in ring]
    area = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        area += x1 * y2 - x2 * y1
    return abs(area) / 2


def geometry_area_sq_km(geometry):
    if not geometry:
        return 0.0
    total = 0.0
    if geometry.get("type") == "Polygon":
        polygons = [geometry.get("coordinates", [])]
    elif geometry.get("type") == "MultiPolygon":
        polygons = geometry.get("coordinates", [])
    else:
        return 0.0
    for polygon in polygons:
        if not polygon:
            continue
        total += ring_area_sq_m(polygon[0])
        for hole in polygon[1:]:
            total -= ring_area_sq_m(hole)
    return max(total / 1_000_000, 0.0)


def centroid_of_geometry(geometry):
    pts = []
    for ring in outer_rings(geometry):
        pts.extend([pt for pt in ring if len(pt) >= 2])
    if not pts:
        return None
    return (sum(pt[0] for pt in pts) / len(pts), sum(pt[1] for pt in pts) / len(pts))


def assign_point_to_area(lon, lat, area_features):
    for area in area_features:
        if point_in_polygon_geometry(lon, lat, area["geometry"]):
            return area
    return None


def write_csv_from_points(fc, path):
    fields = [
        "heritage_id",
        "common_name",
        "scientific_name",
        "location_description",
        "hyperlink",
        "longitude",
        "latitude",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for feature in fc["features"]:
            props = feature["properties"]
            lon, lat = feature["geometry"]["coordinates"][:2]
            row = {field: props.get(field, "") for field in fields}
            row["longitude"] = lon
            row["latitude"] = lat
            writer.writerow(row)


def write_csv_from_feature_properties(fc, path):
    fieldnames = []
    for feature in fc["features"]:
        for key in feature.get("properties", {}).keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for feature in fc["features"]:
            writer.writerow(feature.get("properties", {}))


def build_subzone_density(subzones, trees, hdb_buildings):
    area_features = deepcopy(clean_feature_collection(subzones, {"Polygon", "MultiPolygon"}).get("features", []))
    for feature in area_features:
        feature["geometry"]["_bbox"] = bbox_for_geometry(feature["geometry"])
        props = feature.get("properties", {})
        props["area_sq_km"] = round(geometry_area_sq_km(feature["geometry"]), 4)
        props["heritage_tree_count"] = 0
        props["heritage_trees_per_sq_km"] = 0
        props["hdb_building_count"] = 0
        props["heritage_trees_per_100_hdb_buildings"] = None
        props["tree_proxy_warning"] = "Counts use NParks Heritage Trees as a legal point proxy, not all Singapore trees."
        feature["properties"] = props

    for tree in trees["features"]:
        lon, lat = tree["geometry"]["coordinates"][:2]
        area = assign_point_to_area(lon, lat, area_features)
        if area:
            area["properties"]["heritage_tree_count"] += 1

    hdb_clean = clean_feature_collection(hdb_buildings, {"Polygon", "MultiPolygon"})
    for building in hdb_clean["features"]:
        centroid = centroid_of_geometry(building.get("geometry"))
        if not centroid:
            continue
        area = assign_point_to_area(centroid[0], centroid[1], area_features)
        if area:
            area["properties"]["hdb_building_count"] += 1

    for feature in area_features:
        props = feature["properties"]
        area = props.get("area_sq_km") or 0
        hdb_count = props.get("hdb_building_count") or 0
        if area > 0:
            props["heritage_trees_per_sq_km"] = round(props["heritage_tree_count"] / area, 3)
        if hdb_count > 0:
            props["heritage_trees_per_100_hdb_buildings"] = round(props["heritage_tree_count"] / hdb_count * 100, 3)
        if "_bbox" in feature["geometry"]:
            del feature["geometry"]["_bbox"]
    return {"type": "FeatureCollection", "features": area_features}


def clean_polygon_dataset(fc, keep_fields):
    clean = clean_feature_collection(fc, {"Polygon", "MultiPolygon"})
    out = []
    for feature in clean["features"]:
        props = feature.get("properties", {})
        new_props = {field.lower(): props.get(field) for field in keep_fields if field in props}
        new_props["area_sq_km"] = round(geometry_area_sq_km(feature.get("geometry")), 4)
        out.append({"type": "Feature", "geometry": feature["geometry"], "properties": new_props})
    return {"type": "FeatureCollection", "features": out}


def choose_story_tree(trees):
    preferred = []
    for feature in trees["features"]:
        text = " ".join(str(feature["properties"].get(k, "")) for k in ("common_name", "scientific_name", "location_description", "hyperlink")).lower()
        if "tembusu" in text or "botanic" in text:
            preferred.append(feature)
    chosen = preferred[0] if preferred else trees["features"][0]
    feature = deepcopy(chosen)
    feature["properties"]["story_role"] = "Selected close-up tree for Chapter 5"
    return {"type": "FeatureCollection", "features": [feature]}


def main():
    ensure_dirs()
    raw_paths = {key: download_dataset(key, meta) for key, meta in DATASETS.items()}

    heritage = clean_heritage_trees(load_geojson(raw_paths["heritage_trees"]))
    subzones = load_geojson(raw_paths["subzone_boundary"])
    parks = clean_polygon_dataset(load_geojson(raw_paths["parks_nature_reserves"]), ["OBJECTID", "NAME", "PARK_TYPE", "FMEL_UPD_D"])
    tca = clean_polygon_dataset(load_geojson(raw_paths["tree_conservation_areas"]), ["OBJECTID", "NAME", "REGION", "MORE_INFO", "FMEL_UPD_D"])
    hdb = load_geojson(raw_paths["hdb_existing_buildings"])
    density = build_subzone_density(subzones, heritage, hdb)
    story_tree = choose_story_tree(heritage)

    save_geojson(heritage, PROCESSED_DIR / "heritage_trees.geojson")
    save_geojson(heritage, PROCESSED_DIR / "all_or_proxy_tree_points.geojson")
    save_geojson(density, PROCESSED_DIR / "tree_density_by_subzone.geojson")
    save_geojson(density, PROCESSED_DIR / "tree_access_context_by_subzone.geojson")
    save_geojson(parks, PROCESSED_DIR / "parks_and_nature_reserves.geojson")
    save_geojson(tca, PROCESSED_DIR / "tree_conservation_areas.geojson")
    save_geojson(story_tree, PROCESSED_DIR / "selected_story_tree.geojson")
    write_csv_from_points(heritage, PROCESSED_DIR / "heritage_trees.csv")
    write_csv_from_feature_properties(density, PROCESSED_DIR / "tree_density_by_subzone.csv")

    summary = {
        "heritage_tree_features": len(heritage["features"]),
        "subzone_features": len(density["features"]),
        "parks_nature_reserve_features": len(parks["features"]),
        "tree_conservation_area_features": len(tca["features"]),
        "hdb_building_source_features": len(hdb.get("features", [])),
        "outputs": sorted(p.name for p in PROCESSED_DIR.glob("*")),
    }
    (PROCESSED_DIR / "processing_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
