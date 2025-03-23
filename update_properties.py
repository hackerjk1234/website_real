import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "your-username"
REPO_NAME = "website-real"  # Your repo name
IMAGE_FOLDER = "images/"
PROPERTIES_FILE = "properties.json"

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
                "name": "New Property",
                "address": "Unknown Address",
                "image": image_url,
                "map_link": "https://maps.google.com"
            }
            properties.append(new_entry)

    # Save updated data
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print("✅ properties.json updated successfully!")

if __name__ == "__main__":
    update_properties()
