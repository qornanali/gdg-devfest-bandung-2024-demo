const jwt = require("jsonwebtoken");

const SESSION_SECRET = process.env.SESSION_SECRET || "default-secret-key";

const Error = Object.freeze({
  FIELD_CANNOT_BE_BLANK: "1",
  INVALID_AUTHORIZATION: "2",
});

const validateSession = (req, res, next) => {
  const authorization = req.headers.authorization;

  if (!authorization || !authorization.startsWith("Bearer ")) {
    return res.status(403).json({
      success: false,
      error: {
        code: Error.FIELD_CANNOT_BE_BLANK,
        message: "Authorization is missing or invalid",
        message_title: "Unauthorized",
      },
    });
  }

  const sessionToken = authorization.split(" ")[1];

  try {
    const sessionData = jwt.verify(sessionToken, SESSION_SECRET);

    if (sessionData.ip !== req.ip) {
      throw new Error("IP mismatch");
    }

    req.session = sessionData;
    next();
  } catch (err) {
    return res.status(403).json({
      success: false,
      error: {
        code: Error.INVALID_AUTHORIZATION,
        message: "Your session is invalid or expired. Please reload the page and try again!",
        message_title: "Unauthorized",
      },
    });
  }
};

module.exports = {
  validateSession,
};
