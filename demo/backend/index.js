const express = require("express");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const { loggingMiddleware, errorMiddleware } = require("./middlewares");
const { validateSession } = require("./middlewares/validateSession");
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
app.use(loggingMiddleware());
app.use(cors({
  origin: process.env.ORIGIN_URL,
  credentials: process.env.NODE_ENV === "production",
}));
app.use(cookieParser());
app.use(express.json());

// Routes
app.get("/ping", (req, res) => res.status(201).json({ success: true }));

app.post("/v1/sessions", sessionController.createSession);
app.post("/v1/chat", validateSession, chatController.chatResponse);

// Error middleware
app.use(errorMiddleware());

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
