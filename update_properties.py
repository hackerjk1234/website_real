import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "hackerjk1234"  # Your GitHub username
REPO_NAME = "website-real"  # Your repo name
IMAGE_FOLDER = "images/"  # Folder where images are stored
PROPERTIES_FILE = "properties.json"  # JSON file to update

def update_properties():
    """Automatically updates properties.json with new images"""
    properties = []
    
    # Load existing JSON data if available
    if os.path.exists(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, "r") as f:
            properties = json.load(f)

    # Extract existing image names to avoid duplicates
    existing_images = {prop["image"].split("/")[-1] for prop in properties}

    # Check all images in the folder
    for image in os.listdir(IMAGE_FOLDER):
        if image not in existing_images:
            image_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGE_FOLDER}{image}"
            
            # Placeholder details (update later if needed)
            new_entry = {
                "name": "New Property",  # Replace with actual property name
                "address": "Unknown Address",  # Replace with actual property address
                "image": image_url,
                "map_link": "https://maps.google.com"  # Replace with actual map link if needed
            }
            properties.append(new_entry)

    # Save updated data back to properties.json
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print("✅ properties.json updated successfully!")

if __name__ == "__main__":
    update_properties()
