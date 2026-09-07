# Chapter Plan v1: 500,000 Trees - Singapore's Urban Forest

## Chapter 1: Singapore as an Urban Forest

- Story purpose: Establish Singapore as a heavily managed urban forest and introduce the 500,000+ TreesSG premise within the broader City in Nature agenda.
- Map layer(s): `parks-nature-reserves-fill` at low opacity; optional faint island-wide subzone outline.
- Expected camera scale: Singapore-wide.
- Expected text length: 1-2 short paragraphs.
- Visual elements: Small context legend; optional policy/photo panel if available.
- Data claim: Verified as background only. GovTech describes TreesSG as mapping more than 500,000 urban trees; NParks provides City in Nature policy context. Full all-tree coordinates were not downloaded.

## Chapter 2: Where the Urban Forest Is Protected

- Story purpose: Make the first quantitative claim about official Heritage Tree protection, not all tree distribution.
- Map layer(s): `tree-density-subzone-fill`, `tree-density-subzone-outline`.
- Expected camera scale: Singapore-wide, then slightly closer to the central/southern cluster.
- Expected text length: 1-2 short paragraphs.
- Visual elements: Choropleth legend; optional mini bar chart of top subzones.
- Data claim: Verified for the proxy dataset. `tree_density_by_subzone.geojson` counts 255 NParks Heritage Trees across 332 URA subzones; 66 subzones contain at least one Heritage Tree. Top proxy concentrations include Tyersall/Tanglin, City Hall/Downtown Core, Fort Canning/Museum, Sentosa/Southern Islands and Changi Point/Changi. The chapter must state clearly that this is Heritage Tree proxy density, not all street-tree density.

## Chapter 3: From Tree Density to Everyday Access

- Story purpose: Build directly from Chapter 2: a concentration of trees, especially recognised mature trees, does not automatically mean residents meet trees in everyday neighbourhood life.
- Map layer(s): `tree-access-hdb-context-fill`, `parks-nature-reserves-fill`; optionally dim `tree-density-subzone-fill`.
- Expected camera scale: Planning area / neighbourhood.
- Expected text length: 1-2 short paragraphs.
- Visual elements: Access-context legend; optional callout comparing high-density park/subzone areas with HDB-heavy areas.
- Data claim: Partly verified and conservative. HDB Existing Building centroids were counted by subzone and compared with Heritage Tree proxy counts. Several high proxy-density areas have little or no HDB building context, suggesting that tree concentration can reflect parks, institutions, islands, or nature landscapes rather than everyday residential access. This does not measure walking distance, private housing access, canopy cover, or all street trees.

## Chapter 4: Trees That Carry Memory

- Story purpose: Shift from distribution to value: Heritage Trees are mature, named, protected landmarks that carry ecological, historical, social and aesthetic meaning.
- Map layer(s): `heritage-trees-highlight`, `tree-conservation-areas-fill`, optional `parks-nature-reserves-fill`.
- Expected camera scale: Planning area / neighbourhood clusters.
- Expected text length: 1-2 short paragraphs.
- Visual elements: Point legend; popup/photo links through Heritage Trees URLs.
- Data claim: Verified for official Heritage Tree records. Processed fields include `common_name`, `scientific_name`, `location_description`, `heritage_id`, and `hyperlink`. Manual photo selection still needed.

## Chapter 5: One Tree, One Story

- Story purpose: End with a close, qualitative view so the reader meets one tree as a living urban landmark rather than as a dot in a dataset.
- Map layer(s): `selected-story-tree`; runtime `story-tree-interactive-points`; optional faint park/nature reserve context.
- Expected camera scale: Single tree.
- Expected text length: 1-2 short paragraphs.
- Visual elements: Chengal Pasir photo, linked NParks Heritage Tree profile, and one interactive label card that updates when the reader clicks a nearby Heritage Tree point.
- Data claim: Default tree selected from the official Heritage Tree data: Chengal Pasir / `Hopea odorata Roxb.`, Heritage ID `HT 2015-246`, Singapore Botanic Gardens, Lawn XA. Additional clickable points include Tembusu, Teak, Nemesu, and Saga from NParks Heritage Tree records.

## Suggested `onChapterEnter` / `onChapterExit` Logic

- Chapter 1 enter: `parks-nature-reserves-fill` opacity 0.25.
- Chapter 2 enter: `tree-density-subzone-fill` opacity 0.75, `tree-density-subzone-outline` opacity 0.45; exit by lowering to 0.2 instead of removing instantly.
- Chapter 3 enter: `tree-access-hdb-context-fill` opacity 0.75, `parks-nature-reserves-fill` opacity 0.25, `tree-density-subzone-fill` opacity 0.15.
- Chapter 4 enter: `heritage-trees-highlight` opacity 1, `tree-conservation-areas-fill` opacity 0.35; lower Chapter 3 layers.
- Chapter 5 enter: `selected-story-tree` opacity 1; keep only faint context layers.
