# whitelee-wind-constraints-qgis
(Write up in progress)

Constraint mapping for onshore wind at Whitelee, south of Glasgow. Used QGIS to identify constraint-free land and calculated summary statistics using PyQGIS. 
## Background
The Scottish Government's ambition for installed capacity of onshore wind in Scotland has been set to at least 20 GW by 2030 (Scottish Government, 2022). This was set out in the Onshore Wind Policy Statement 2022, which also stressed the importance of developments that preserve the natural environment. Locational constraint mapping can be used to address both of these ambitions. 
## Aim
To identify constraint-free land for wind farm development at Whitelee, south of Glasgow.
## Study Area
The study area is centred approximately 22 km south of Glasgow city centre, covering an area of 400 km<sup>2</sup> (20 x 20 km). Surrounding towns include Newton Mearns, Kilmarnock and East Kilbride. The grid extent is Easting 246,000 – 266,000 m and Northing 634,000 – 654,000 m (British National Grid, EPSG:27700). 

The area is made up of various landscape types with most of it consisting of moorland (62.59%); the rest is a mixture of farmland, river valleys and some urban areas. These groups were derived from NatureScot's Landscape Character Types (Scottish Natural Heritage, 2019). 
## Methods
Open data was combined in QGIS to create a locational constraint layer to identify constraint-free land. PyQGIS measured the constraint-free areas and obtained summary statistics.  

### 1. Software and coordinate reference system 
- Software: QGIS 3.44.15 and PyQGIS.
- CRS: EPSG:27700 - OSGB36 / British National Grid. Used by these layers: roads, buildings, water, woodland, peat, protected areas (SSSI, SPA, SAC), DTM and all subsequent layers created from them. 
- Basemap: EPSG:3857 WGS 84 / Pseudo-Mercator (used for display purposes).
- Existing turbines: Originally in EPSG:4326 - WGS 84. The turbines were reprojected to EPSG:27700 to match the other layers. 
- British National Grid is the standard grid for Great Britain and the OS and NatureScot data were already supplied in it. 
- A metre-based CRS was essential for creating buffer distances and area calculations. 

### 2. Data Preparation

| Dataset | Clipped to (tool) | Other preparation |
|---|---|---|
| Study Area | Easting 246,000 - 266,000, Northing 634,000 - 654,000  | Buffered layer to create new 1 km buffer boundary surrounding the study area to avoid edge effects |
| OS OpenMap Local | study area 1 km buffer layer (Clip) |  |
| OS Open Roads | study area 1 km buffer layer (Clip) |  |
| Carbon and Peatland 2016 map | study area 1 km buffer layer (Clip) | Filtered IMPORTANCE field to classes 1 and 2 and 181 features remained |
| SSSIs, SPAs, SACs | study area 1 km buffer layer (Clip) | Layers were merged (Merge tool) as they all followed the same rule of exclusion if present. No SACs, 4 SSSIs and 1 SPA within study area |
| OS Terrain 50 | study area (Clip Raster by Extent) | Nine DTM tiles (NS43-45, NS53-55, NS63-65) were merged. |
| OpenStreetMap Turbines | study area (Clip) | Reprojected to EPSG:27700, then clipped |
| Landscape Character Assessment | study area (Clip) | Added 'Area_km<sup>2</sup>' and 'LCT_Group' fields |

## 3. Constraint criteria
Maximum proposed turbine dimensions were selected from the Whitelee Repowering Scoping Report (ScottishPower Renewables, 2026).
- Hub height: 164 m
- Rotor radius: 86 m 
- Tip height: 250 m

| Constraint | Rule | Reason |
|---|---|---|
| Buildings | 500 m buffer | As the Scottish Government's written answer stated that there is no recommended minimum distance between onshore wind turbines and residential properties, I chose a 500 m buffer from Welsh Assembly Government guidance as a separation distance for noise (Scottish Parliament, 2023; Welsh Assembly Government, 2005, Annex D, p.59).  |
| Woodland | 136 m buffer | Buffer to protect bat populations and reduce the risk of collisions. I created a simplified, precautionary buffer: I used NatureScot's guidance of a 50 m clearance buffer and added this to the rotor radius (50 m plus the 86 m rotor radius, giving 136 m) (NatureScot, 2021; ScottishPower Renewables, 2026). (See Limitations) |
| Roads tier 1: Motorways, trunk, A roads | 375 m buffer | I selected a 375 m buffer based on correspondence from Transport Scotland,  who asked East Lothian Council to require sites to be a minimum of 1.5 x tip height from kerb line of trunk roads; 1.5 x 250 m = 375 m (Transport Scotland, 2013). The letter included this requirement for trunk roads only, which prompted me to make a tiered buffer system for road types. Applied this choice to motorways and A roads as a precautionary simplification, as trunk roads are primarily motorways and major A roads (Traffic Scotland, n.d.).  |
| Roads tier 2: B, minor, local roads, local access and secondary access roads  | 250 m buffer | As I found no Scottish minimum, I based the 250 m buffer choice on Rutland County Council, to account for fall-over distance: tip height (Rutland County Council, 2012).  |
| Roads tier 3: Restricted local access roads | None  | Based on my judgement. Upon inspection of OS Open Roads, these roads were mainly for private use as tracks for Whitelee wind farm within the study area.  |
| Water | 50 m buffer | Cautious choice based on a previous project by SP Energy Networks, who chose a 50 m buffer around each watercourse in their scoping consultation, from which they based on SEPA's recommendations (SP Energy Networks, 2023a) |
| Peat | Importance Classes 1 & 2 | No buffer. Filtered to only include importance classes 1 and 2, regarded as land dominated by rich peat soil and peatland habitats (NatureScot, 2026; Scottish Government, Scottish Natural Heritage, SEPA, 2017). |
| Protected areas | No buffer, SSSI + SPA (no SACs in area) | No buffer; excluded where present, precautionary screen (Scottish Government, 2023). |
| Slope | Steeper than 15°  | No buffer; excluded slopes steeper than 15 degrees, based on Welsh Government guidance (Welsh Assembly Government, 2005, Annex D, p.58).  |

## Results
## Maps
1. Interactive web map 1. Extent of locational constraints at Whitelee. Link: https://arcg.is/9LvW02

2. Interactive web map 2. Whitelee constraint-free areas and existing turbines. Link:  https://arcg.is/0HnDqH2

## Script
## Data Sources and Licences

| Dataset | Provider | Acknowledgement | Licence | Use |
|---|---|---|---|---|
| OS OpenMap Local | Ordnance Survey | Contains OS data © Crown copyright and database right 2026 | OS OpenData | Constraint: buildings, woodlands and surface water |
| OS Open Roads | Ordnance Survey | Contains OS data © Crown copyright and database right 2026 | OS OpenData | Roads constraint |
| Carbon and Peatland 2016 map | NatureScot (SNH) and the James Hutton Institute | Carbon and Peatland 2016 map, © SNH and JHI. Map produced by SNH using data from the James Hutton Institute, used with permission, all rights reserved. UK Non-Commercial Government Licence v2.0. | Non-Commercial Government Licence v2.0 | Peat classes 1 and 2 |
| SSSIs, SPAs, SACs | NatureScot (SNH) | Protected Areas: SSSIs, SPAs, SACs (Copyright Scottish Natural Heritage). Contains OS data © Crown copyright and database right (2022, 2023). Available under the Open Government Licence v3.0. | OGL v3.0 | Protected areas constraint, no SACs fall within study area |
| OS Terrain 50 | Ordnance Survey | Contains OS data © Crown copyright and database right 2026 | OS OpenData | Slope (>15 degrees) |
| OpenStreetMap | OpenStreetMap contributors | © OpenStreetMap contributors, openstreetmap.org/copyright. | ODbL | Existing turbines and basemap |
| Landscape Character Assessment | NatureScot (SNH) |  | OGL v3.0 | Landscape types (Study Area description) |

Raw data is not included in the repository and can be downloaded from each provider.
## References
Scottish Government (2022). *Onshore wind: policy statement 2022*. Available at: https://www.gov.scot/publications/onshore-wind-policy-statement-2022/ (Accessed: 8 November 2026).  

Scottish Natural Heritage (2019). *Landscape Character Assessment 2019*. [dataset]. Available at: https://opendata.nature.scot/datasets/18520effe11a4cffa0f22f19a22ac57a_0 (Accessed: 8 November 2026).

ScottishPower Renewables (2026). Whitelee Windfarm Repowering: Scoping Report. Submitted 24 July 2026. Energy Consents Unit case ECU00006441. Available at: https://energyconsents.scot/ApplicationDetails.aspx?cr=ECU00006441 (Accessed: 23/10/2026).


## AI Use (Fair-Use Statement)
