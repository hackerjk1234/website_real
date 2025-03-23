import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "hackerjk1234"
REPO_NAME = "website-real"  # Your repo name
IMAGE_FOLDER = "images/"
PROPERTIES_FILE = "properties.json"

def load_property_details():
    """Load property details from property_details.txt"""
    properties = []
    with open("property_details.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                # Split the line at the first colon (:)
                image, details = line.split(":", 1)
                
                # Now split details into name and address by separating at the first comma
                parts = details.split(",", 1)  # Split only at the first comma
                if len(parts) == 2:
                    name, address = map(str.strip, parts)
                else:
                    name = parts[0].strip()
                    address = ""  # If no comma found, treat as a single field (possible bug)

                # Append the property data
                properties.append({
                    "name": name,
                    "address": address,
                    "image": f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGE_FOLDER}{image.strip()}",
                    "map_link": f"https://maps.google.com/?q={address.replace(' ', '+')}"
                })
    return properties

def update_properties():
    """Automatically updates properties.json with new images"""
    # Load existing JSON data if available
    if os.path.exists(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, "r") as f:
            properties = json.load(f)
    else:
        properties = []

    # Load new property details
    new_properties = load_property_details()

    # Extract existing image names to avoid duplicates
    existing_images = {prop["image"].split("/")[-1] for prop in properties}

    # Check all new properties and add them if not already added
    for prop in new_properties:
        image_name = prop["image"].split("/")[-1]
        if image_name not in existing_images:
            properties.append(prop)

    # Save updated data to properties.json
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print("✅ properties.json updated successfully!")

if __name__ == "__main__":
    update_properties()
