const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
const port = 3000;

// Create 'images' directory if it doesn't exist
const imagesDir = path.join(__dirname, "images");
if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
}

// Setup Multer for file storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, imagesDir); // Store files in 'images' folder
    },
    filename: (req, file, cb) => {
        const ext = path.extname(file.originalname);
        const uniqueName = `${Date.now()}_${Math.random().toString(36).substring(7)}${ext}`;
        cb(null, uniqueName);
    },
});

const upload = multer({ storage, limits: { fileSize: 2 * 1024 * 1024 } }); // 2MB file size limit

// Serve static files (images) from the 'images' folder
app.use("/images", express.static(imagesDir));

// Simple form for uploading files
app.get("/", (req, res) => {
    res.send(`
        <html>
            <body>
                <h2>Upload Property Image</h2>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="text" name="name" placeholder="Property Name" required><br><br>
                    <input type="text" name="address" placeholder="Property Address" required><br><br>
                    <input type="file" name="image" accept="image/*" required><br><br>
                    <button type="submit">Upload</button>
                </form>
            </body>
        </html>
    `);
});

// Handle file upload
app.post("/upload", upload.single("image"), (req, res) => {
    if (!req.file) {
        return res.status(400).send("No file uploaded.");
    }

    const { name, address } = req.body;
    const uploadedFileUrl = `/images/${req.file.filename}`;

    // Respond with success message and file URL
    res.send(`
        <h2>Upload Successful</h2>
        <p>Property Name: ${name}</p>
        <p>Property Address: ${address}</p>
        <p><img src="${uploadedFileUrl}" alt="Property Image" width="300"></p>
        <p><a href="/">Go back</a></p>
    `);
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
