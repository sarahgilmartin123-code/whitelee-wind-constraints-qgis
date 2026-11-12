# whitelee-wind-constraints-qgis
(Write up in progress)

Constraint mapping for onshore wind at Whitelee, south of Glasgow. Used QGIS to identify constraint-free land and calculated summary statistics using PyQGIS. 
## Background
The Scottish Government's ambition for installed capacity of onshore wind in Scotland has been set to at least 20 GW by 2030 (Scottish Government, 2022). This was set out in the Onshore Wind Policy Statement 2022, which also stressed the importance of developments that preserve the natural environment. Locational constraint mapping can be used to address both of these ambitions. 
## Aim
To identify constraint-free land for wind farm development at Whitelee, south of Glasgow.
## Study Area
The study area is centred approximately 22 km south of Glasgow city centre, covering an area of 400 km<sup>2</sup> (20 by 20 km). Surrounding towns include Newton Mearns, Kilmarnock and East Kilbride. The grid extent is Easting 246,000 – 266,000 m and Northing 634,000 – 654,000 m (British National Grid, EPSG:27700). 

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


## Results
## Maps
## Script
## Data Sources and Licences

| Dataset | Provider | Acknowledgement | Licence | Use |
|---|---|---|---|---|
| OS OpenMap Local | Ordnance Survey | Contains Ordnance Survey data © Crown copyright and database right 2026 | OS OpenData | Constraint: buildings, woodlands and surface water |
| OS Open Roads | Ordnance Survey | Contains Ordnance Survey data © Crown copyright and database right 2026 | OS OpenData | Roads constraint |
| Carbon and Peatland 2016 map | NatureScot (SNH) and the James Hutton Institute | Carbon and Peatland 2016 map, © SNH and JHI. Map produced by SNH using data from the James Hutton Institute, used with permission, all rights reserved. UK Non-Commercial Government Licence, version 2. | Non-Commercial Government Licence v2 | Peat classes 1 and 2 |
| SSSIs, SPAs, SACs | NatureScot (SNH) | Protected Areas: SSSIs, SPAs, SACs (Copyright Scottish Natural Heritage) Contains Ordnance Survey data © Crown copyright and database right (2022, 2023). Available under the Open Government Licence v3.0. | OGL v3.0 | Protected areas constraint |
| OS Terrain 50 | Ordnance Survey | Contains Ordnance Survey data © Crown copyright and database right 2026 | OS OpenData | Slope (>15 degrees) |
| OpenStreetMap | OpenStreetMap contributors | © OpenStreetMap contributors, openstreetmap.org/copyright. | ODbL | Existing turbines and basemap |
| Landscape Character Assessment | NatureScot (SNH) | © SNH, contains Ordnance Survey data © Crown copyright and database right (2021). Available under the Open Government Licence v3.0. | OGL v3.0 | Landscape types (Study Area description) |

Raw data is not included in the repository and can be downloaded from each provider.
## References
Scottish Government (2022). *Onshore wind: policy statement 2022*. Available at: https://www.gov.scot/publications/onshore-wind-policy-statement-2022/ (Accessed: 8 November 2026).  

Scottish Natural Heritage (2019). *Landscape Character Assessment 2019*. [dataset]. Available at: https://opendata.nature.scot/datasets/18520effe11a4cffa0f22f19a22ac57a_0 (Accessed: 8 November 2026).
## AI Use (Fair-Use Statement)
