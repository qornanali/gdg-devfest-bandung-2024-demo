const express = require("express");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const { validateSession } = require("./middlewares/session");
const { handleThrownError } = require("./middlewares/error");
const { logReqResp } = require("./middlewares/logging");
const sessionController = require("./controllers/sessionController");
const chatController = require("./controllers/chatController");
const dotenv = require("dotenv");
const app = express();

console.log(`Initializing app ${process.env.NODE_ENV}`);

// Load environment variables
if (process.env.NODE_ENV !== "production" && process.env.NODE_ENV !== "staging") {
  console.log("Loading environment variables from .env file");
  dotenv.config();
}

// Constants
const PORT = process.env.PORT || 3000;

// Middleware
app.use(logReqResp());
app.use(cors({
  origin: process.env.ORIGIN_URL,
  credentials: process.env.NODE_ENV === "production",
}));
app.use(cookieParser());
app.use(express.json());

// Routes
app.get("/ping", (req, res) => res.status(201).json({ success: true }));

app.post("/v1/sessions", sessionController.createSession);
app.post("/v1/chat", validateSession, chatController.generateChat);

// Error middleware
app.use(handleThrownError());

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
