const chatResponse = (req, res) => {
    res.status(201).json({
      success: true,
      data: {
        message: `Hello, how can I help you? ${req.requestId}`,
        created_time: Date.now(),
      },
    });
  };
  
  module.exports = {
    chatResponse,
  };
  