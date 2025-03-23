import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "hackerjk1234"  # Your GitHub username
REPO_NAME = "website_real"  # Your repo name
IMAGE_FOLDER = "images/"
PROPERTIES_FILE = "properties.json"
PROPERTY_DETAILS_FILE = "property_details.txt"  # File to store property details

def load_property_details():
    """Load property details from the text file"""
    property_details = []
    if os.path.exists(PROPERTY_DETAILS_FILE):
        with open(PROPERTY_DETAILS_FILE, "r") as file:
            for line in file.readlines():
                parts = line.strip().split(":")
                if len(parts) == 2:
                    image_file, address = parts
                    # Splitting the address into name and address part
                    name, address = address.split(",", 1)
                    property_details.append({
                        "name": name.strip(),
                        "address": address.strip(),
                        "image": f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGE_FOLDER}{image_file.strip()}",
                        "map_link": f"https://maps.google.com/?q={address.strip()}"
                    })
    return property_details

def update_properties():
    """Automatically updates properties.json with new images"""
    properties = load_property_details()

    # Save updated data to properties.json
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print("✅ properties.json updated successfully!")

if __name__ == "__main__":
    update_properties()
