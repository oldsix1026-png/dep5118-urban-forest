# Data Sources: 500,000 Trees - Singapore's Urban Forest

Prepared on 2026-09-07 for DEP5118 ITA2 Phase 1.

## Source Inventory

| Dataset | Source URL | Download method | Reported data date / update | Project use | Reliability and limits |
|---|---|---|---|---|---|
| NParks Heritage Trees | https://data.gov.sg/datasets/d_644ff187b6d14d6316f47284a4a6c81f/view | data.gov.sg `poll-download` API | Data from Oct 2025; data.gov.sg page crawled 2026-09 reports last updated 22 Aug 2026 | Official point layer for Heritage Trees; extracted common name, scientific name, location description, heritage id and hyperlink | High reliability for gazetted Heritage Trees. It is not a full tree inventory and cannot support claims about every street tree. |
| URA Master Plan 2019 Subzone Boundary (No Sea) | https://data.gov.sg/datasets/d_8594ae9ff96d0c708bc2af633048edfb/view | data.gov.sg `poll-download` API | Data from Sep 2021; data.gov.sg page reports last updated 3 Dec 2025 | Spatial aggregation unit for tree count/density and HDB context | High reliability for planning geography. Boundaries are indicative planning boundaries and may not match local lived neighbourhood edges. |
| NParks Parks and Nature Reserves | https://data.gov.sg/datasets/d_77d7ec97be83d44f61b85454f844382f/view | data.gov.sg `poll-download` API | data.gov.sg citation page retrieved 2026-09-07; third-party index showed 2026-09-03 update | Green-space context overlay for Chapter 3 | High reliability as official NParks park/nature reserve geometry. It explains green-space context but does not count individual trees. |
| NParks Tree Conservation Area | https://data.gov.sg/datasets/d_52b9eabe398353bd6acd9aee15b13f72/view | data.gov.sg `poll-download` API | Data from Sep 2016; data.gov.sg page reports last updated 17 Dec 2025 | Conservation policy context overlay for Chapter 4 | High reliability for indicative extent of the two gazetted TCAs. It marks conservation zones, not individual tree locations. |
| HDB Existing Building | https://data.gov.sg/datasets/d_16b157c52ed637edd6ba1232e026258d/view | data.gov.sg `poll-download` API | Data from Nov 2025; page reports last updated 21 Jun 2026 | Conservative residential/everyday access proxy for Chapter 3; building centroids counted by subzone | High reliability for HDB building footprints. It does not represent all residences, private housing, population, or walking distance. |
| TreesSG / all urban trees | https://www.nparks.gov.sg/treessg | Public web map reviewed, no bulk download used | TreesSG page last updated 22 Feb 2026 in search result; GovTech article describes 500,000+ mapped trees in 2018 | Background claim for story framing only | TreesSG is authoritative for public exploration and the 500,000+ premise, but no clearly documented open bulk download/API was found in this pass. No restricted scraping was performed. |
| GovTech article on TreesSG | https://www.tech.gov.sg/technews/the-inside-story-of-how-nparks-mapped-500000-trees-in-singapore-on-treessg/ | Web reference | Published 23 May 2018 | Citation for "500,000 trees" framing and TreesSG background | Useful secondary official-government explainer. It supports the story premise but is not a downloadable geospatial dataset. |
| NParks City in Nature key strategies | https://www.nparks.gov.sg/who-we-are/city-in-nature-key-strategies | Web reference | Page seen 2026-09-07 | Chapter 1 context for City in Nature framing | Official policy context. Use for background, not spatial analysis. |

## Cleaning Notes

- All processed files are written as WGS84 GeoJSON, suitable for Mapbox upload.
- Empty geometries, unsupported geometry types, out-of-Singapore point coordinates and duplicate Heritage Tree IDs were removed.
- Heritage Tree fields were normalised into `heritage_id`, `common_name`, `scientific_name`, `location_description`, `hyperlink`, `source_objectid`, `source_updated`.
- Subzone polygon areas were estimated in square kilometres using a local equirectangular approximation appropriate for Singapore-scale comparison.
- `tree_density_by_subzone.geojson` and `tree_access_context_by_subzone.geojson` use NParks Heritage Trees as the legal point proxy, plus HDB building counts by subzone. They should be labelled as proxy analysis, not complete tree density.

## Current Processed Counts

- Heritage Tree points: 255
- Subzones: 332
- Subzones with at least one Heritage Tree: 66
- Parks and nature reserve polygons: 462
- Tree Conservation Areas: 2
- HDB building polygons used for subzone context: 13,436

