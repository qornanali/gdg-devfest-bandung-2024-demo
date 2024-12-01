const { v4: uuidv4 } = require("uuid");

const loggingMiddleware = () => (req, res, next) => {
  const start = Date.now();
  req.requestId = req.headers["request-id"] || uuidv4();
  const { method, url } = req;

  console.log(
    `Request request-id=${req.requestId}: [${new Date().toISOString()}] ${method} ${url}`
  );

  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(
      `Response request-id=${req.requestId}: [${new Date().toISOString()}] ${method} ${url} - ${res.statusCode} (${duration}ms)`
    );
  });

  next();
};

const errorMiddleware = () => (err, req, res, next) => {
  console.error(
    `Error request-id=${req.requestId}: [${new Date().toISOString()}] stack: ${err.stack}`
  );
  res.status(500).json({
    success: false,
    error: {
      code: "900",
      message: "There is an unexpected error. Please try again!",
      message_title: "Internal Server Error",
    },
  });
};

module.exports = {
  loggingMiddleware,
  errorMiddleware,
};
