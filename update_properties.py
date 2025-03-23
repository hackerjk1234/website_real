import os
import json

# 🏡 GitHub repo details
GITHUB_USERNAME = "hackerjk1234"
REPO_NAME = "website-real"  # Your repo name
IMAGE_FOLDER = "images/"
PROPERTIES_FILE = "properties.json"
PROPERTY_DETAILS_FILE = "property_details.txt"  # The new text file for property details

def load_property_details():
    """Load property details from the text file."""
    property_details = {}
    if os.path.exists(PROPERTY_DETAILS_FILE):
        with open(PROPERTY_DETAILS_FILE, "r") as f:
            for line in f:
                # Example line: "image1.jpg: Luxury Villa, 123 Sunset Blvd, Thanjavur"
                parts = line.strip().split(":", 1)
                if len(parts) == 2:
                    image_name = parts[0].strip()
                    # Now split the remaining part by the first comma (property name and address)
                    name_and_address = parts[1].split(",", 1)
                    if len(name_and_address) == 2:
                        name = name_and_address[0].strip()  # The property name before the first comma
                        address = name_and_address[1].strip()  # The address after the first comma
                        property_details[image_name] = {"name": name, "address": address}
                    else:
                        # If the address does not have a comma (should not happen with valid data)
                        print(f"Skipping invalid entry in {PROPERTY_DETAILS_FILE}: {line}")
    return property_details

def update_properties():
    """Automatically updates properties.json with new images and their details."""
    properties = []
    
    # Load existing JSON data if available
    if os.path.exists(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, "r") as f:
            properties = json.load(f)

    # Extract existing image names to avoid duplicates
    existing_images = {prop["image"].split("/")[-1] for prop in properties}

    # Load property details from the text file
    property_details = load_property_details()

    # Check all images in the folder
    for image in os.listdir(IMAGE_FOLDER):
        if image not in existing_images:
            image_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGE_FOLDER}{image}"
            
            # Get property details from the loaded dictionary, if available
            details = property_details.get(image, {"name": "New Property", "address": "Unknown Address"})
            
            new_entry = {
                "name": details["name"],
                "address": details["address"],
                "image": image_url,
                "map_link": f"https://maps.google.com/?q={details['address']}"
            }
            properties.append(new_entry)

    # Save updated data
    with open(PROPERTIES_FILE, "w") as f:
        json.dump(properties, f, indent=4)

    print("✅ properties.json updated successfully!")

if __name__ == "__main__":
    update_properties()
