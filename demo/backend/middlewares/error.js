const { ErrorCode } = require("../constants/errorCodes");

const handleThrownError = () => (err, req, res, next) => {
  console.error(
    `Error request-id=${req.requestId}: [${new Date().toISOString()}] stack: ${err.stack}`
  );
  res.status(500).json({
    success: false,
    error: {
      code: ErrorCode.GENERIC_ERROR,
      message: "There is an unexpected error. Please try again!",
      message_title: "Internal Server Error",
    },
  });
};

module.exports = {
  handleThrownError,
};
