import json
import os

# File paths
PROPERTY_DETAILS_FILE = "property_details.txt"
PROPERTIES_JSON_FILE = "properties.json"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/hackerjk1234/website_real/main/images/"

def load_property_details():
    """Reads property details from property_details.txt and returns a list of dictionaries."""
    properties = []
    try:
        with open(PROPERTY_DETAILS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                parts = line.split(":")
                if len(parts) < 2:
                    print(f"Skipping invalid line: {line}")
                    continue  # Skip malformed lines

                image_filename = parts[0].strip()
                details = ":".join(parts[1:]).strip()

                # Ensure there are exactly 2 parts after splitting by comma
                detail_parts = details.split(",")
                if len(detail_parts) < 2:
                    print(f"Skipping line with missing details: {line}")
                    continue  # Skip invalid lines

                name = detail_parts[0].strip()
                address = ",".join(detail_parts[1:]).strip()

                # Construct full image URL
                image_url = IMAGE_BASE_URL + image_filename

                # Construct Google Maps search link
                map_link = f"https://maps.google.com/?q={address.replace(' ', '+')}"

                properties.append({
                    "name": name,
                    "address": address,
                    "image": image_url,
                    "map_link": map_link
                })

                # Limit to 10 properties
                if len(properties) >= 10:
                    break

    except FileNotFoundError:
        print(f"Error: {PROPERTY_DETAILS_FILE} not found.")
    
    return properties

def update_properties():
    """Updates properties.json with data from property_details.txt."""
    new_properties = load_property_details()

    # Debugging: Print parsed properties
    print("Parsed properties:", json.dumps(new_properties, indent=4))

    # Write to properties.json
    with open(PROPERTIES_JSON_FILE, "w") as f:
        json.dump(new_properties, f, indent=4)

    print(f"Updated {PROPERTIES_JSON_FILE} successfully!")

if __name__ == "__main__":
    update_properties()
