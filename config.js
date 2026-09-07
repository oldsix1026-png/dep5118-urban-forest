var config = {
    style: 'mapbox://styles/oldsix666/cmtqzcff100fs01qy5ltpch7x',
    accessToken: 'pk.eyJ1Ijoib2xkc2l4NjY2IiwiYSI6ImNtdHF6MXBiaDEycWoyeW9rcHZoaTM1cmUifQ.l_RTeA-vi_rnbr6K85sDIg',
    showMarkers: false,
    markerColor: '#2f8f5b',
    inset: false,
    theme: 'light',
    use3dTerrain: false,
    auto: false,
    title: "500,000 Trees: Singapore's Urban Forest",
    subtitle: 'Trees as city infrastructure, everyday access, and living heritage',
    byline: 'By Zhou Jiaxuan',
    footer: 'Sources: NParks, URA, HDB, data.gov.sg, TreesSG and GovTech Singapore. Heritage Trees are used as an official point proxy where complete street-tree downloads are not openly available.',
    storyTrees: [
        {
            id: 'chengal-pasir',
            commonName: 'Chengal Pasir',
            scientificName: 'Hopea odorata',
            heritageId: 'HT 2015-246',
            location: 'Singapore Botanic Gardens, Lawn XA',
            coordinates: [103.8154093, 1.3159576],
            url: 'https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2015-246/',
            image: './assets/chengal-pasir.png',
            photoAlt: 'Chengal Pasir Heritage Tree in Singapore Botanic Gardens',
            photoCaption: 'Chengal Pasir Heritage Tree, Singapore Botanic Gardens.'
        },
        {
            id: 'tembusu',
            commonName: 'Tembusu',
            scientificName: 'Cyrtophyllum fragrans',
            heritageId: 'HT 2001-26',
            location: 'Singapore Botanic Gardens, Lawn E',
            coordinates: [103.8167908, 1.3085458],
            url: 'https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2001-26/',
            image: './assets/tembusu.jpg',
            photoAlt: 'Tembusu Heritage Tree in Singapore Botanic Gardens',
            photoCaption: 'Tembusu Heritage Tree in 2024. Photo: Hazri Boey / NParks.'
        },
        {
            id: 'teak',
            commonName: 'Teak',
            scientificName: 'Tectona grandis',
            heritageId: 'HT 2014-234',
            location: 'Singapore Botanic Gardens, along Office Ring Road, Botany Centre',
            coordinates: [103.8179930, 1.3082486],
            url: 'https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2014-234/',
            image: './assets/teak.jpg',
            photoAlt: 'Teak Heritage Tree in Singapore Botanic Gardens',
            photoCaption: 'Teak Heritage Tree. Photo: Brendon Phuah / NParks.'
        },
        {
            id: 'nemesu',
            commonName: 'Nemesu',
            scientificName: 'Rubroshorea pauciflora',
            heritageId: 'HT 2015-245',
            location: 'Singapore Botanic Gardens, Rainforest',
            coordinates: [103.8168939, 1.3110444],
            url: 'https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2015-245/',
            image: './assets/nemesu.jpg',
            photoAlt: 'Nemesu Heritage Tree in Singapore Botanic Gardens Rainforest',
            photoCaption: 'Nemesu Heritage Tree crown. Photo: Hazri Boey / NParks.'
        },
        {
            id: 'saga',
            commonName: 'Saga',
            scientificName: 'Adenanthera pavonina',
            heritageId: 'HT 2001-19',
            location: 'Singapore Botanic Gardens, near Frangipani Garden',
            coordinates: [103.8170589, 1.3098950],
            url: 'https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2001-19/',
            image: './assets/saga.jpg',
            photoAlt: 'Saga Heritage Tree in Singapore Botanic Gardens',
            photoCaption: 'Saga Heritage Tree in 2024. Photo: Hazri Boey / NParks.'
        }
    ],
    initialLayerState: [
        { layer: 'tree-density-subzone-fill', opacity: 0, duration: 0 },
        { layer: 'tree-density-subzone-outline', opacity: 0, duration: 0 },
        { layer: 'tree-access-hdb-context-fill', opacity: 0, duration: 0 },
        { layer: 'heritage-trees-highlight', opacity: 0, duration: 0 },
        { layer: 'parks-nature-reserves-fill', opacity: 0, duration: 0 },
        { layer: 'tree-conservation-areas-fill', opacity: 0, duration: 0 },
        { layer: 'selected-story-tree', opacity: 0, duration: 0 },
        { layer: 'tree-conservation-areas', opacity: 0, duration: 0 }
    ],
    chapters: [
        {
            id: 'singapore-urban-forest',
            alignment: 'left',
            hidden: false,
            title: 'Singapore as an Urban Forest',
            description: 'Singapore is often described as the City in Nature. This map begins from a wider question: trees are not only scenery, but part of the city\'s everyday infrastructure.<br><br>This view shows parks and nature reserves with a faint heritage-tree density context. These green spaces form the base of the urban forest, but the next question is how recognised trees are distributed, and who meets them in daily life.',
            legendImage: './assets/legend-overview.svg',
            legendAlt: 'Legend showing parks and faint heritage tree density',
            location: {
                center: [103.8198, 1.3521],
                zoom: 10.35,
                pitch: 0,
                bearing: 0
            },
            mapAnimation: 'flyTo',
            rotateAnimation: false,
            callback: '',
            onChapterEnter: [
                { layer: 'parks-nature-reserves-fill', opacity: 0.22, duration: 1100 },
                { layer: 'tree-density-subzone-fill', opacity: 0.10, duration: 1100 },
                { layer: 'tree-density-subzone-outline', opacity: 0.05, duration: 1100 },
                { layer: 'tree-access-hdb-context-fill', opacity: 0, duration: 700 },
                { layer: 'heritage-trees-highlight', opacity: 0, duration: 700 },
                { layer: 'tree-conservation-areas-fill', opacity: 0, duration: 700 },
                { layer: 'selected-story-tree', opacity: 0, duration: 700 }
            ],
            onChapterExit: [
                { layer: 'parks-nature-reserves-fill', opacity: 0.08, duration: 700 }
            ]
        },
        {
            id: 'where-trees-concentrate',
            alignment: 'left',
            hidden: false,
            title: 'Where the Urban Forest Is Protected',
            description: 'The story now moves from general greenery to trees with official heritage value. These are not all of Singapore\'s trees; they are mature trees that NParks has recorded and protected as Heritage Trees.<br><br>This map uses Heritage Trees per square kilometre by subzone. The strongest clusters appear in places such as Tyersall, Fort Canning, and City Hall, where parks, history, institutions, and landscape value overlap.<span class="data-note">This is a Heritage Tree proxy, not a map of all street trees.</span>',
            legendImage: './assets/legend-density.svg',
            legendAlt: 'Legend for heritage tree proxy density by subzone',
            location: {
                center: [103.8375, 1.3145],
                zoom: 11.35,
                pitch: 0,
                bearing: 0,
                speed: 1.7
            },
            mapAnimation: 'flyTo',
            rotateAnimation: false,
            callback: '',
            onChapterEnter: [
                { layer: 'tree-density-subzone-fill', opacity: 0.78, duration: 1200 },
                { layer: 'tree-density-subzone-outline', opacity: 0.48, duration: 1200 },
                { layer: 'parks-nature-reserves-fill', opacity: 0.06, duration: 900 },
                { layer: 'tree-access-hdb-context-fill', opacity: 0, duration: 800 },
                { layer: 'heritage-trees-highlight', opacity: 0, duration: 800 },
                { layer: 'tree-conservation-areas-fill', opacity: 0, duration: 800 },
                { layer: 'selected-story-tree', opacity: 0, duration: 800 }
            ],
            onChapterExit: [
                { layer: 'tree-density-subzone-fill', opacity: 0.18, duration: 900 },
                { layer: 'tree-density-subzone-outline', opacity: 0.18, duration: 900 }
            ]
        },
        {
            id: 'density-to-everyday-access',
            alignment: 'right',
            hidden: false,
            title: 'From Tree Density to Everyday Access',
            description: 'A high Heritage Tree cluster does not always mean residents meet those trees every day. Some clusters sit in parks, institutions, tourism areas, or subzones with few HDB buildings.<br><br>This map compares Heritage Trees with HDB building context, using Heritage Trees per 100 HDB buildings as an access proxy. It is not a walking-distance model, but it helps separate protected tree landscapes from trees near daily housing routes.',
            legendImage: './assets/legend-access.svg',
            legendAlt: 'Legend for heritage trees per 100 HDB buildings',
            location: {
                center: [103.8450, 1.3330],
                zoom: 11.85,
                pitch: 24,
                bearing: -8,
                speed: 1.6
            },
            mapAnimation: 'flyTo',
            rotateAnimation: false,
            callback: '',
            onChapterEnter: [
                { layer: 'tree-access-hdb-context-fill', opacity: 0.76, duration: 1200 },
                { layer: 'parks-nature-reserves-fill', opacity: 0.24, duration: 1200 },
                { layer: 'tree-density-subzone-fill', opacity: 0.10, duration: 900 },
                { layer: 'tree-density-subzone-outline', opacity: 0.22, duration: 900 },
                { layer: 'heritage-trees-highlight', opacity: 0, duration: 800 },
                { layer: 'tree-conservation-areas-fill', opacity: 0, duration: 800 },
                { layer: 'selected-story-tree', opacity: 0, duration: 800 }
            ],
            onChapterExit: [
                { layer: 'tree-access-hdb-context-fill', opacity: 0.10, duration: 900 },
                { layer: 'parks-nature-reserves-fill', opacity: 0.10, duration: 900 }
            ]
        },
        {
            id: 'heritage-trees',
            alignment: 'left',
            hidden: false,
            title: 'Trees That Carry Memory',
            description: 'Trees can be infrastructure and heritage at the same time. After looking at density and access, this view returns to the individual protected trees behind the pattern.<br><br>The processed NParks dataset contains 255 Heritage Trees. Tree Conservation Areas add a wider protection layer, showing places where mature-tree landscapes are treated as part of Singapore\'s identity and planning.',
            legendImage: './assets/legend-heritage.svg',
            legendAlt: 'Legend for heritage trees and tree conservation areas',
            location: {
                center: [103.8200, 1.3095],
                zoom: 13.05,
                pitch: 35,
                bearing: 12,
                speed: 1.55
            },
            mapAnimation: 'flyTo',
            rotateAnimation: false,
            callback: '',
            onChapterEnter: [
                { layer: 'heritage-trees-highlight', opacity: 0.95, duration: 1200 },
                { layer: 'tree-conservation-areas-fill', opacity: 0.34, duration: 1200 },
                { layer: 'parks-nature-reserves-fill', opacity: 0.12, duration: 900 },
                { layer: 'tree-density-subzone-fill', opacity: 0.05, duration: 800 },
                { layer: 'tree-access-hdb-context-fill', opacity: 0, duration: 800 },
                { layer: 'selected-story-tree', opacity: 0, duration: 800 }
            ],
            onChapterExit: [
                { layer: 'tree-conservation-areas-fill', opacity: 0.12, duration: 800 },
                { layer: 'heritage-trees-highlight', opacity: 0.26, duration: 800 }
            ]
        },
        {
            id: 'one-tree-one-story',
            alignment: 'right',
            hidden: false,
            title: 'One Tree, One Story',
            description: 'The final view stops at Chengal Pasir, <em>Hopea odorata</em>, Heritage ID HT 2015-246, in Singapore Botanic Gardens. The map is now at the scale of a single tree and the path around it.<br><br>Here, the urban forest is no longer an island-wide pattern. It is a tall trunk, shade, a signboard, and a protected living landmark that people can stand beside. Click another nearby point to meet a different Heritage Tree. <a class="read-more" href="https://heritagetrees.nparks.gov.sg/heritagetrees/ht-2015-246/" target="_blank" rel="noopener noreferrer">Read more</a>',
            legendImage: './assets/legend-story-tree.svg',
            legendAlt: 'Legend for the selected story tree',
            location: {
                center: [103.8162, 1.3121],
                zoom: 16.05,
                pitch: 56,
                bearing: 24,
                speed: 1.35
            },
            mapAnimation: 'flyTo',
            rotateAnimation: true,
            callback: '',
            showStoryTrees: true,
            onChapterEnter: [
                { layer: 'selected-story-tree', opacity: 0, duration: 700 },
                { layer: 'heritage-trees-highlight', opacity: 0, duration: 700 },
                { layer: 'parks-nature-reserves-fill', opacity: 0.16, duration: 700 },
                { layer: 'tree-conservation-areas-fill', opacity: 0.08, duration: 700 },
                { layer: 'tree-density-subzone-fill', opacity: 0, duration: 700 },
                { layer: 'tree-density-subzone-outline', opacity: 0, duration: 700 },
                { layer: 'tree-access-hdb-context-fill', opacity: 0, duration: 700 }
            ],
            onChapterExit: [
                { layer: 'selected-story-tree', opacity: 0, duration: 700 }
            ]
        }
    ]
};
