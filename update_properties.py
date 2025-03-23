import json

# File paths
PROPERTY_DETAILS_FILE = "property_details.txt"
OUTPUT_JSON_FILE = "properties.json"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/hackerjk1234/website_real/main/images/"

def load_property_details():
    properties = []
    with open(PROPERTY_DETAILS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            try:
                image_filename, details = line.split(":", 1)
                name, address = details.split(",", 1)

                # Construct the correct raw image URL
                image_url = f"{GITHUB_RAW_URL}{image_filename.strip()}?raw=true"

                property_data = {
                    "name": name.strip(),
                    "address": address.strip(),
                    "image": image_url,
                    "map_link": f"https://maps.google.com/?q={address.strip().replace(' ', '+')}"
                }
                properties.append(property_data)
            except ValueError:
                print(f"Skipping invalid line: {line}")  # Error handling for incorrect format

    return properties

def update_properties():
    new_properties = load_property_details()

    # Write to properties.json
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(new_properties, f, indent=4)

    print(f"Updated {OUTPUT_JSON_FILE} with {len(new_properties)} properties.")

if __name__ == "__main__":
    update_properties()
