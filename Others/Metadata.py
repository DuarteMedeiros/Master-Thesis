import geopandas as gpd

# Replace 'your_shapefile.shp' with the path to your shapefile
shapefile_path = r"CnclDist_July2012.shp"

print("READ")

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Access metadata
metadata = gdf.metadata

# Display metadata
print(metadata)
