const fs = require("fs");
const path = require("path");
const formidable = require("formidable");

// Access the secret key from the environment variable
const SECRET_KEY = process.env.UPLOAD_SECRET || "default-secret";  // Default in case the environment variable is not set

exports.handler = async (event) => {
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: JSON.stringify({ error: "Method Not Allowed" }) };
    }

    // Log secret key for debugging purposes
    console.log("Secret Key from Environment:", SECRET_KEY);  // This will log the environment variable's value
    
    // Validate Secret Key
    const headers = event.headers || {};
    if (headers["x-upload-secret"] !== SECRET_KEY) {
        console.log("Received Secret Key:", headers["x-upload-secret"]);
        return { statusCode: 403, body: JSON.stringify({ error: "Invalid Secret Key" }) };
    }

    // Parse Form Data
    const form = new formidable.IncomingForm({ maxFileSize: 2 * 1024 * 1024 }); // 2MB limit

    return new Promise((resolve, reject) => {
        form.parse(event, async (err, fields, files) => {
            if (err) {
                return resolve({ statusCode: 400, body: JSON.stringify({ error: "File Upload Error" }) });
            }

            // Get File & Property Details
            const { name, address } = fields;
            const file = files.image;

            if (!file) {
                return resolve({ statusCode: 400, body: JSON.stringify({ error: "No Image Provided" }) });
            }

            // Validate File Type
            const allowedTypes = ["image/jpeg", "image/png", "image/gif", "image/webp"];
            if (!allowedTypes.includes(file.mimetype)) {
                return resolve({ statusCode: 400, body: JSON.stringify({ error: "Invalid File Type" }) });
            }

            // Create 'images' Folder if Not Exists
            const imagesDir = path.join(__dirname, "../../images");
            if (!fs.existsSync(imagesDir)) {
                fs.mkdirSync(imagesDir, { recursive: true });
            }

            // Generate Unique File Name
            const fileExt = path.extname(file.originalFilename);
            const uniqueFileName = `${Date.now()}_${Math.random().toString(36).substring(7)}${fileExt}`;
            const filePath = path.join(imagesDir, uniqueFileName);

            // Move File to 'images' Directory
            fs.renameSync(file.filepath, filePath);

            // Return Success Response
            return resolve({
                statusCode: 200,
                body: JSON.stringify({
                    message: "File Uploaded Successfully",
                    fileName: uniqueFileName,
                    propertyName: name || "Unknown Property",
                    address: address || "Unknown Address",
                    url: `/images/${uniqueFileName}`
                })
            });
        });
    });
};
