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

### 3. Constraint criteria
Maximum proposed turbine dimensions were selected from the Whitelee Repowering Scoping Report (ScottishPower Renewables, 2026).
- Hub height: 164 m
- Rotor radius: 86 m 
- Tip height: 250 m

| Constraint | Rule | Reason |
|---|---|---|
| Buildings | 500 m buffer | As the Scottish Government's written answer stated that there is no recommended minimum distance between onshore wind turbines and residential properties, I chose a 500 m buffer from Welsh Assembly Government guidance as a separation distance for noise (Scottish Parliament, 2023; Welsh Assembly Government, 2005, Annex D, p. 59).  |
| Woodland | 136 m buffer | Buffer to protect bat populations and reduce the risk of collisions. I created a simplified, precautionary buffer: I used NatureScot's guidance of a 50 m clearance buffer and added this to the rotor radius (50 m plus the 86 m rotor radius, giving 136 m) (NatureScot, 2021; ScottishPower Renewables, 2026) (see Limitations). |
| Roads tier 1: Motorways, trunk, A roads | 375 m buffer | I selected a 375 m buffer based on correspondence from Transport Scotland,  who asked East Lothian Council to require sites to be a minimum of 1.5 x tip height from kerb line of trunk roads; 1.5 x 250 m = 375 m (Transport Scotland, 2013). The letter included this requirement for trunk roads only, which prompted me to make a tiered buffer system for road types. I applied this choice to motorways and A roads as a precautionary simplification, as trunk roads are primarily motorways and major A roads (Traffic Scotland, n.d.).  |
| Roads tier 2: B, minor, local roads, local access and secondary access roads  | 250 m buffer | As I found no Scottish minimum, I based the 250 m buffer choice on Rutland County Council, to account for fall-over distance: tip height (Rutland County Council, 2012).  |
| Roads tier 3: Restricted local access roads | None  | Based on my judgement. Upon inspection of OS Open Roads, these roads were mainly for private use as tracks for Whitelee wind farm within the study area.  |
| Water | 50 m buffer | Cautious choice based on SEPA's recommendation in a scoping consultation for SP Energy Networks, suggesting a 50 m buffer around each watercourse (SP Energy Networks, 2023a). |
| Peat | Importance Classes 1 & 2 | No buffer. Filtered to only include importance classes 1 and 2, regarded as land dominated by rich peat soil and peatland habitats (NatureScot, 2026; Scottish Government, Scottish Natural Heritage, SEPA, 2017). |
| Protected areas | No buffer, SSSI + SPA (no SACs in area) | No buffer; excluded where present, precautionary screen (Scottish Government, 2023). |
| Slope | Steeper than 15°  | No buffer; excluded slopes steeper than 15 degrees, based on Welsh Government guidance (Welsh Assembly Government, 2005, Annex D, p. 58).  |

### 4. Combining the constraints

Each vector layer was rasterised using the 'Rasterise (Vector to Raster)' tool. All rasterised vector layers were set to the same setting to allow them to be combined seamlessly, as set out below: 

- A fixed value to burn: 1. 

- Output extent: Easting 246,000 – 266,000 m and Northing 634,000 – 654,000 m.

The output extent was set to that of the study area. 

- Width and Height resolution: 50 x 50 m.

These values were used to match the OS Terrain 50 dataset, to maintain the alignment of slope values.
  
- NoData value to output bands: -9999.

When rasterising the buildings layer, QGIS had set a NoData value of 0 to output bands, which resulted in only 66% of the area being outputted, as it excluded all area with a value of 0. The project's method relies on cells having a value of 0 or 1, constraint-free or constrained, respectively. Adding the constraints would produce the total number of all constraints present within that cell. If cells were given a NoData value, the raster calculator would have outputted a NoData value. To overcome this, a NoData value of -9999 was set, a value that lies outwith the datasets. This value was applied to the settings of all rasterised vector layers to ensure that every cell with value 0 maintained its value. 

- Output data type: Float32.

Type was chosen in line with all other raster types, to avoid issues when layers are combined. 

- CRS: EPSG: 27700 British National Grid.

Following this, the merged DTM layer was used to obtain slope values using the 'slope' tool. The z factor was set to 1 as both the height and horizontal units (EPSG: 27700) were in metres. The 'Raster Calculator' tool was used to group slope values: slope values > 15° = 1; slopes ≤ 15° = 0, which was outputted to create a new layer, c_slope. When the new slope layer was compared with the OS basemap, a small white patch that corresponds to a steep sloped area was identifiable on the slope layer, which correlated with Loudon Hill on the OSM basemap.  


The 'Raster Calculator' tool was used to add all raster layers together, to obtain a raster count for each 50m cell. The following expression was used:

"c_buildings@1" + "c_peat@1" + "c_protected@1" + "c_roads@1" + "c_slope@1" + "c_water@1" + "c_woodland@1"


Settings: 
- Output extent: set to the study site 
- Resolution: 400 columns by 400 rows
- Output CRS: EPSG:27700, British National Grid in line with all other data and the output layer was saved as constraints_total

## Results

- STATISTICS_MINIMUM=0
- STATISTICS_MAXIMUM=5
- STATISTICS_MEAN=2.1097
- STATISTICS_STDDEV=0.97339786829437
- STATISTICS_VALID_PERCENT=100

The constraints_total layer had a range from 0 to 5. Statistics are shown in the table of all constraint layers statistics below. To check validity of the data, the sum of all means of the individual constraint layers were added up and the result matched with the mean of constraints_total. The extent and pixel size were also checked for accuracy. 

- Cells per score (0 to 5): 

Next, the number of cells at each score were counted using the Raster layer unique values report. 

| Layer | Rule | Min | Max | Valid (%) | Mean | % of study area | km2 (mean x 400) |
|---|---|---|---|---|---|---|---|
| c_buildings | 500 m buffer | 0 | 1 | 100 | 0.6647 | 66.47% | 265.86 |
| c_woodland | 136 m buffer | 0 | 1 | 100 | 0.5935 | 59.35% | 237.42 |
| c_roads | Tiered: 375 / 250 / 0 m | 0 | 1 | 100 | 0.4102 | 41.02% | 164.07 |
| c_water | 50 m buffer | 0 | 1 | 100 | 0.3161 | 31.61% | 126.44 |
| c_peat | Importance Classes 1 & 2 | 0 | 1 | 100 | 0.1020 | 10.20% | 40.78 |
| c_protected | No buffer, SSSI +SPA (no SACs in area) | 0 | 1 | 100 | 0.0200 | 2.00% | 7.98 |
| c_slope | >15 degrees (excluded) | 0 | 1 | 100 | 0.0033 | 0.33% | 1.33 |
| Total |  |  |  |  | 2.1097 | 0.00% | 0.00 |
| Combined Raster Count |  | 0 | 5 | 100 | 2.1097 (SD 0.97) | 0.00% | 0.00 |

The table below displays the total raster count for each cell. 
| "Value" | "Cell count" | "m2" | "km2" | "% of study area" |
|---|---|---|---|---|
| 0 | 4211 | 10527500 | 10.53 | 263.19% |
| 1 | 41932 | 104830000 | 104.83 | 2620.75% |
| 2 | 59141 | 147852500 | 147.85 | 3696.31% |
| 3 | 41758 | 104395000 | 104.40 | 2609.88% |
| 4 | 12726 | 31815000 | 31.82 | 795.38% |
| 5 | 232 | 580000 | 0.58 | 14.50% |


## Maps
1. Interactive web map 1. Extent of locational constraints at Whitelee. Link: https://arcg.is/9LvW02

2. Interactive web map 2. Whitelee constraint-free areas and existing turbines. Link:  https://arcg.is/0HnDqH2

## Limitations
This is a simplified, independent project, not a real planning or site assessment. 

- Woodland buffer: NatureScot recommended a 50 m clearance between blade tip and woodland, using a formula that included hub height, blade length and tree height (NatureScot, 2021). Instead, I measured it horizontally, adding the 50 m to the 86 m rotor radius, excluding hub and tree height. As a result, it is likely that my buffer is larger than the formula would have produced, therefore excluding usable land. This choice was made to keep the project straightforward and approach with caution.
- Surface water buffer: A 50 m water buffer was used, based on recommendations by SEPA for an SP Energy Networks overhead line project (SP Energy Networks, 2023a). However, the project's final design used a 10 m buffer because the number of small watercourses and drains meant that the larger buffer wasn't able to be met, due to spacing requirements between towers (SP Energy Networks, 2023b). Therefore, the 50 m buffer likely excludes more land than a real-world project would use.
- Building buffer: Since OpenMap Local did not give information on building use, all entries were treated equally and given the same buffer. Therefore, land that was usable may have been omitted as a result of the cautious approach. This could be improved by use of data that records building use, to exclude homes without a noise buffer.
- OS Terrain 50 dataset: The dataset will give a more generalised view of the terrain as its designed to work with more small-scale products (Ordnance Survey, 2013). This could result in some areas that are steeper than 15 degrees being identified as meeting the slope threshold. Steep sloped terrain such as Loudoun Hill was identified, however, smaller steep slopes could have been missed. 

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
| Landscape Character Assessment | NatureScot (SNH) | © SNH , contains Ordnance Survey data © Crown copyright and database right (2021) | OGL v3.0 | Landscape types (Study Area description) |

Raw data is not included in the repository and can be downloaded from each provider.
## References

Ordnance Survey (2013). OS terrain 50 user guide, version 1.0. Available at: https://digimap.edina.ac.uk/help/files/resource-hub/downloads/osmanuals/os-terrain-50-user-guide_v1.0.pdf (Accessed: 20th November 2026).

NatureScot (2021). Bats and onshore wind turbines: survey assessment and mitigation. Available at: https://www.nature.scot/bats-and-onshore-wind-turbines-survey-assessment-and-mitigation#7.1.2%C2%A0+Buffers-01 (Accessed: 23rd October 2026).

NatureScot (2026). Advising on peatland habitats and carbon-rich soils in development management. Available at: https://www.nature.scot/doc/advising-peatland-habitats-and-carbon-rich-soils-development-management (Accessed: 23rd October 2026).

Rutland County Council (2012). Wind Turbine Developments: Supplementary Planning Document. Oakham: Rutland County Council. Adopted 12/11/2012. Available at: https://www.rutland.gov.uk/sites/default/files/2022-12/Wind%20Turbines%20SPD%20%282012%29.pdf (Accessed: 23rd October 2026).

Scottish Government (2022). *Onshore wind: policy statement 2022*. Available at: https://www.gov.scot/publications/onshore-wind-policy-statement-2022/ (Accessed: 8th November 2026).  

Scottish Government (2023). National Planning Framework 4. Edinburgh: Scottish Government. Available at: https://www.gov.scot/publications/national-planning-framework-4/ (Accessed: 24th October 2026).

Scottish Government, Scottish Natural Heritage, SEPA (2017). Peatland Survey. Guidance on Developments on Peatland, on-line version only. Available at: https://www.gov.scot/binaries/content/documents/govscot/publications/advice-and-guidance/2018/12/peatland-survey-guidance/documents/peatland-survey-guidance-2017/peatland-survey-guidance-2017/govscot%3Adocument/Guidance%2Bon%2Bdevelopments%2Bon%2Bpeatland%2B-%2Bpeatland%2Bsurvey%2B-%2B2017.pdf (Accessed: 24th October 2026). 

Scottish Natural Heritage (2019). *Landscape Character Assessment 2019*. [dataset]. Available at: https://opendata.nature.scot/datasets/18520effe11a4cffa0f22f19a22ac57a_0 (Accessed: 8th November 2026).

Scottish Parliament (2023). Written question and answer S6W-20063, answered 14 August 2023. Available at: https://www.parliament.scot/chamber-and-committees/questions-and-answers/question?ref=S6W-20063 (Accessed: 24th October 2026)

ScottishPower Renewables (2026). Whitelee Windfarm Repowering: Scoping Report. Energy Consents Unit case ECU00006441. Available at: https://www.scottishpowerrenewables.com/documents/d/guest/Whitelee_Windfarm_Repowering_Scoping_Report (Accessed: 23rd October 2026).

SP Energy Networks (2023a). 'Appendix 7.1: Watercourse Crossings and Buffers', in The Glenmuckloch to Glenglass
Reinforcement Project: Environmental Impact Assessment Report, Volume 4. Available at:  https://www.spenergynetworks.co.uk/userfiles/file/Volume_4_Appendix_7.1_Watercourse_Crossings.pdf (Accessed: 24th October 2026). 

SP Energy Networks (2023b). The Glenmuckloch to Glenglass
Reinforcement Project: Environmental Impact Assessment Report: Non-Technical Summary. January 2023. Available at: https://www.spenergynetworks.co.uk/userfiles/file/EIA_Report_Non-Technical_Summary.pdf (Accessed: 23rd October 2026).

Traffic Scotland (n.d.). Trunk road network. Available at: https://www.traffic.gov.scot/trunk-roads (Accessed: 24th October 2026).

Transport Scotland (2013). Consultation on East Lothian Guidance for wind farms over twelve megawatts [letter to East Lothian Council, 17/05/2013]. Available at: https://eastlothianconsultations.co.uk/housing-environment/12mw_wind_spg/results/response-transport-scotland_redacted.pdf (Accessed: 23rd October 2026).

Welsh Assembly Government (2005). Planning Policy Wales: Technical Advice Note 8: Planning for Renewable Energy. Cardiff: Welsh Assembly Government. Available at: https://www.gov.wales/sites/default/files/publications/2018-09/tan8-renewable-energy_0.pdf  (Accessed: 23rd October 2026).

## AI Use (Fair-Use Statement)
