const jwt = require("jsonwebtoken");

const SESSION_SECRET = process.env.SESSION_SECRET || "default-secret-key";
const SESSION_EXPIRATION = parseInt(process.env.SESSION_EXPIRATION, 10) || 3600;

const Error = Object.freeze({
  FIELD_CANNOT_BE_BLANK: "1",
  INVALID_AUTHORIZATION: "2",
});

const createSession = (req, res) => {
  const authorization = req.headers.authorization;

  if (!authorization || !authorization.startsWith("Basic ")) {
    return res.status(403).json({
      success: false,
      error: {
        code: Error.FIELD_CANNOT_BE_BLANK,
        message: "Authorization is missing or invalid",
        message_title: "Unauthorized",
      },
    });
  }

  const credentialToken = authorization.split(" ")[1];
  if (credentialToken !== process.env.CREDENTIAL_TOKEN) {
    return res.status(403).json({
      success: false,
      error: {
        code: Error.INVALID_AUTHORIZATION,
        message: "Invalid credentials",
        message_title: "Unauthorized",
      },
    });
  }

  const sessionData = { ip: req.ip };
  const sessionToken = jwt.sign(sessionData, SESSION_SECRET, { expiresIn: SESSION_EXPIRATION });

  res.status(201).json({
    success: true,
    data: {
      value: sessionToken,
      expires_in: SESSION_EXPIRATION,
    },
  });
};

module.exports = {
  createSession,
};
