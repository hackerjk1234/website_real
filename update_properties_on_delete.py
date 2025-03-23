import json
import os

# File paths
IMAGES_FOLDER = "images"
PROPERTIES_FILE = "properties.json"

def update_properties():
    # Load existing properties.json
    try:
        with open(PROPERTIES_FILE, "r", encoding="utf-8") as file:
            properties = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: properties.json not found or corrupted.")
        return

    # Get current image filenames
    existing_images = set(os.listdir(IMAGES_FOLDER))

    # Filter out entries where images no longer exist
    updated_properties = [
        property for property in properties if os.path.basename(property["image"]) in existing_images
    ]

    # Check if properties.json needs updating
    if len(updated_properties) != len(properties):
        with open(PROPERTIES_FILE, "w", encoding="utf-8") as file:
            json.dump(updated_properties, file, indent=4)
        print("properties.json updated successfully.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    update_properties()
