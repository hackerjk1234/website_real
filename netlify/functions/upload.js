const fs = require("fs");
const path = require("path");
const formidable = require("formidable");

// 🔐 Set a Secret Key to Allow Uploads (Change this!)
const SECRET_KEY = "akdfjLJ29fj2912o0i2j";

// 📂 Ensure images directory exists
const IMAGE_DIR = "images/";
if (!fs.existsSync(IMAGE_DIR)) {
    fs.mkdirSync(IMAGE_DIR, { recursive: true });
}

exports.handler = async (event) => {
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    const form = new formidable.IncomingForm();
    
    return new Promise((resolve) => {
        form.parse(event, (err, fields, files) => {
            if (err) {
                return resolve({ statusCode: 500, body: "Error processing form" });
            }

            // ✅ Secret Key Check
            if (fields.key !== SECRET_KEY) {
                return resolve({ statusCode: 403, body: "Unauthorized" });
            }

            // 📸 Check for Image File
            const image = files.propertyImage;
            if (!image) {
                return resolve({ statusCode: 400, body: "No image uploaded" });
            }

            // ✅ Allowed File Extensions
            const allowedExtensions = [".jpg", ".jpeg", ".png"];
            const ext = path.extname(image.originalFilename).toLowerCase();
            if (!allowedExtensions.includes(ext)) {
                return resolve({ statusCode: 400, body: "Invalid file type" });
            }

            // ✅ Limit File Size to 2MB
            if (image.size > 2 * 1024 * 1024) {
                return resolve({ statusCode: 400, body: "File too large" });
            }

            // 🏡 Property Name & Address
            const propertyName = fields.propertyName || "Unknown Property";
            const propertyAddress = fields.propertyAddress || "Unknown Address";

            // 🔄 Generate Unique Image Name
            const uniqueFileName = `${Date.now()}-${image.originalFilename}`;
            const filePath = path.join(IMAGE_DIR, uniqueFileName);

            // 🚀 Move Image to Images Folder
            fs.rename(image.filepath, filePath, (err) => {
                if (err) {
                    return resolve({ statusCode: 500, body: "Error saving file" });
                }

                // 📌 Append New Property to JSON
                const propertiesPath = "properties.json";
                let properties = [];

                if (fs.existsSync(propertiesPath)) {
                    properties = JSON.parse(fs.readFileSync(propertiesPath));
                }

                properties.push({
                    name: propertyName,
                    address: propertyAddress,
                    image: `/images/${uniqueFileName}`,
                });

                fs.writeFileSync(propertiesPath, JSON.stringify(properties, null, 2));

                return resolve({ statusCode: 200, body: "Property added successfully!" });
            });
        });
    });
};
