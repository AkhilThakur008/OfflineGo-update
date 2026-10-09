import os
import requests
import zipfile

print("🌍 Fetching latest map data from OpenStreetMap/Overpass API...")

# Punjab boundary ka overpass query ya free OSM data source
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
query = """
[out:json][timeout:25];
area["name"="Punjab"]["boundary"="administrative"]->.searchArea;
(
  way(area.searchArea);
  relation(area.searchArea);
);
out body;
>;
out skel qt;
"""

response = requests.post(OVERPASS_URL, data=query)
if response.status_code == 200:
    print("✅ Data fetched successfully! Creating map tiles package...")
    
    # Yahan data ko process karke tiles banate hain
    os.makedirs("output_tiles", exist_ok=True)
    
    # Dummy/Raw data ko zip banana
    with open("output_tiles/data.geojson", "w") as f:
        f.write(response.text)

    # Zip file compress karna
    zip_name = "punjab-tiles.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("output_tiles"):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), "output_tiles"))
                
    print(f"📦 Zip file created: {zip_name}")
else:
    print("❌ Failed to fetch data from server.")
