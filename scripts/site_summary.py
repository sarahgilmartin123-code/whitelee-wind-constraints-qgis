constraint_free_areas = QgsProject.instance().mapLayersByName('constraint_free_areas')[0]
print(f"Total no. polygons in layer: {constraint_free_areas.featureCount()} ")

turbines_study_area = QgsProject.instance().mapLayersByName('turbines_study_area')[0]
print(f"Existing turbines in the study area: {turbines_study_area.featureCount()}")

# Study area box 20km x 20km (400km2)
study_area_km2 = 400

# Minimum site size: 3 turbines x 0.83km2 (20MW threshold) 
min_site_size_km2 = 2.49

# create loop for constraint-free polygons to print those where DN = 1
tot_area_km2 = 0
site_count = 0
largest_area_km2 = 0

for polygon in constraint_free_areas.getFeatures():
    if polygon["DN"] == 1:
        area_km2 = polygon.geometry().area()/1000000
        tot_area_km2 = tot_area_km2 + area_km2 
        if area_km2 >= min_site_size_km2:
            site_count = site_count + 1
        if area_km2 > largest_area_km2:
            largest_area_km2 = area_km2
        
print(f"Total Constraint-free land: {tot_area_km2:.2f} km²")
print(f"{site_count} candidate sites that are >={min_site_size_km2}km²")
print(f"Largest area: {largest_area_km2:.2f}km²")

pct_constraint_free = (tot_area_km2 / study_area_km2)*100

print(f"{pct_constraint_free:.2f}% of the study site is constraint-free")

# Counting existing turbines on constraint-free areas
turbines_on_free_land = 0

for turbine in turbines_study_area.getFeatures():
    for polygon in constraint_free_areas.getFeatures():
        if polygon["DN"] == 1 and polygon.geometry().contains(turbine.geometry()):
            turbines_on_free_land = turbines_on_free_land + 1
 
print(f"{turbines_on_free_land} existing turbines on constraint-free land")
pct_turbines_free_land = (turbines_on_free_land / turbines_study_area.featureCount())*100
print(f"{pct_turbines_free_land:.2f}% of the turbines in the study area are on constraint-free land")
