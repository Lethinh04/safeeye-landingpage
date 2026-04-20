const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// EJS template engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "src/view"));

// Static files
app.use(express.static(path.join(__dirname, "public")));

// ─── Routes ───────────────────────────────
app.get("/", (req, res) => res.render("index", { title: "SafeEye – Đôi mắt thông minh cho người khiếm thị" }));



// ─── Start ────────────────────────────────
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`\n┌─────────────────────────────────────────┐`);
        console.log(`│  SafeEye Web Server                       │`);
        console.log(`│  http://localhost:${PORT}/                 │`);
        console.log(`│                                           │`);
        console.log(`└─────────────────────────────────────────┘\n`);
    });
}

// Cần thiết để Vercel nhận diện đây là một Serverless Function
module.exports = app;
