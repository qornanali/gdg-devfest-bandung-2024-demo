const { v4: uuidv4 } = require("uuid");

const logReqResp = () => (req, res, next) => {
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

module.exports = {
    logReqResp
};
