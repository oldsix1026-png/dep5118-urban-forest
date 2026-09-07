# Mapbox Upload Plan

The processed files live in `ITA2/urban-forest/data/processed`. Upload these through Mapbox Studio as tilesets, then add them to one custom style for the Mapbox Storytelling template.

## Tilesets and Suggested Layers

| File | Suggested tileset name | Studio layer name | Layer type | Styling | Initial opacity |
|---|---|---|---|---|---|
| `tree_density_by_subzone.geojson` | `sg-tree-density-subzone` | `tree-density-subzone-fill` | Fill | Choropleth by `heritage_trees_per_sq_km`; 0 = transparent pale grey, low = `#cfe8b5`, mid = `#78b66b`, high = `#227344`, very high = `#084c2e`; outline `#ffffff` at 0.35 | 0 |
| `tree_density_by_subzone.geojson` | `sg-tree-density-subzone` | `tree-density-subzone-outline` | Line | `#24513f`, width 0.5 | 0 |
| `tree_access_context_by_subzone.geojson` | `sg-tree-access-context-subzone` | `tree-access-hdb-context-fill` | Fill | Diverging/step style using `heritage_trees_per_100_hdb_buildings`; no HDB buildings = muted grey `#d7d7d0`; low = `#f2d9a0`; medium = `#8fc6a5`; high = `#276749` | 0 |
| `all_or_proxy_tree_points.geojson` | `sg-tree-proxy-points` | `tree-proxy-points` | Circle | Circle radius 3-5; color `#155f3b`; stroke `#ffffff`, stroke width 0.8; label popup fields: `common_name`, `scientific_name`, `location_description` | 0 |
| `heritage_trees.geojson` | `sg-heritage-trees` | `heritage-trees-highlight` | Circle | Circle radius 5-8; color `#f2b705`; stroke `#412f00`, stroke width 1 | 0 |
| `parks_and_nature_reserves.geojson` | `sg-parks-nature-reserves` | `parks-nature-reserves-fill` | Fill | Fill `#2f8f5b`, opacity 0.25-0.45; outline `#1d5f40` | 0 |
| `tree_conservation_areas.geojson` | `sg-tree-conservation-areas` | `tree-conservation-areas-fill` | Fill | Fill `#7b4fa3`, opacity 0.25; outline `#4b246f`, dash line if using a line layer | 0 |
| `selected_story_tree.geojson` | `sg-selected-story-tree` | `selected-story-tree` | Circle + symbol | Circle radius 10-14; color `#ff6b35`; stroke `#ffffff`, stroke width 2; optional label from `common_name` | 0 |

## Story Layer Choreography

Use `onChapterEnter` / `onChapterExit` in `config.js` so the map has a clear visual progression:

1. Chapter 1: show `parks-nature-reserves-fill` at low opacity and optionally a very faint `tree-density-subzone-fill`.
2. Chapter 2: fade in `tree-density-subzone-fill` and `tree-density-subzone-outline`; keep points off so the first quantitative layer reads as a choropleth.
3. Chapter 3: fade Chapter 2 choropleth down, fade in `tree-access-hdb-context-fill`, and overlay `parks-nature-reserves-fill` at low opacity. This asks whether high tree proxy density aligns with everyday residential context.
4. Chapter 4: fade in `heritage-trees-highlight` and `tree-conservation-areas-fill`; reduce the context layers.
5. Chapter 5: show only `selected-story-tree` plus a soft park/context basemap, then zoom to single-tree scale.

## Legend Text

- Chapter 2 legend: "Heritage tree proxy density by subzone: trees per sq km. Higher values indicate concentrations of officially recognised mature trees, not all street trees."
- Chapter 3 legend: "Heritage tree proxy per 100 HDB buildings. Grey areas have no HDB building footprints in the dataset."
- Chapter 4 legend: "Heritage Trees and Tree Conservation Areas: protected or recognised mature-tree landscapes."
- Chapter 5 legend: "Selected story tree: close-up qualitative anchor."

## Upload Checks

- After upload, check that Mapbox reads numeric fields as numbers: `heritage_tree_count`, `heritage_trees_per_sq_km`, `hdb_building_count`, `heritage_trees_per_100_hdb_buildings`.
- Set all custom layers to visible in Studio but with 0 opacity before using scrollytelling. The template changes opacity at scroll time.
- Keep Studio layer IDs exactly aligned with the names above or update `config.js` to match your final IDs.

