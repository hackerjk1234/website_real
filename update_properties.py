import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "hackerjk1234"
REPO_NAME = "website-real"  # Your repo name
IMAGE_FOLDER = "images/"
PROPERTIES_FILE = "properties.json"

def load_property_details():
    """Load property details from the text file."""
    properties = []
    with open('property_details.txt', 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split(":")
                if len(parts) == 2:  # Ensure there's only one ':' per line
                    image, details = parts
                    details = details.strip()
                    name, address = map(str.strip, details.split(","))
                    properties.append({
                        "image": image.strip(),
                        "name": name,
                        "address": address,
                        "map_link": f"https://maps.google.com/?q={address.replace(' ', '+')}"
                    })
                else:
                    print(f"Skipping invalid line: {line.strip()}")
    return properties

def update_properties():
    """Automatically updates properties.json with new images"""
    properties = []
    
    # Load existing JSON data if available
    if os.path.exists(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, "r") as f:
            properties = json.load(f)

    # Extract existing image names to avoid duplicates
    existing_images = {prop["image"].split("/")[-1] for prop in properties}

    # Load new property details
    new_properties = load_property_details()

    print(f"Loaded {len(new_properties)} properties from the text file.")  # Debug line

    # Check all images in the folder
    for property_data in new_properties:
        image = property_data["image"]
        if image not in existing_images:
            image_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGE_FOLDER}{image}"
            new_entry = {
                "name": property_data["name"],
                "address": property_data["address"],
                "image": image_url,
                "map_link": property_data["map_link"]
            }
            properties.append(new_entry)

    # Save updated data
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print(f"✅ properties.json updated successfully with {len(properties)} properties.")

if __name__ == "__main__":
    update_properties()
