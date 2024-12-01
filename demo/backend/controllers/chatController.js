const axios = require("axios");
const { ErrorCode } = require("../constants/errorCodes");

const generateChat = async (req, res) => {
  try {
    const { message } = req.body;
    if (!message || message.trim() === '') {
      return res.status(400)
      .json({
        success: false,
        error: {
          code: ErrorCode.FIELD_CANNOT_BE_BLANK,
          message: "Message cannot be blank.",
          message_title: "Bad Request",
        }
      });
    }

    // Read environment variables
    const geminiBaseUrl = process.env.GEMINI_AI_BASE_URL;
    const geminiApiKey = process.env.GEMINI_AI_API_KEY;
    const geminiModelId = process.env.GEMINI_AI_MODEL_ID;
    const temperature = parseFloat(process.env.TEMPERATURE || '0.2');
    const maxOutputTokens = parseInt(process.env.MAX_OUTPUT_TOKENS || '30', 10);
    const topP = parseFloat(process.env.TOP_P || '0.8');
    const topK = parseInt(process.env.TOP_K || '3', 10);

    // Prepare request payload
    const payload = {
      contents: [
        {
          role: 'user',
          parts: [
            {
              text: message,
            },
          ],
        },
      ],
      safetySettings: [
        { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
        { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
        { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
        { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
      ],
      generationConfig: {
        stopSequences: [],
        temperature,
        maxOutputTokens,
        topP,
        topK,
      },
    };

    // Make POST request to Gemini AI API
    console.log('Making request to Gemini AI API:', payload);
    const response = await axios.post(
      `${geminiBaseUrl}/v1beta/models/${geminiModelId}:generateContent?key=${geminiApiKey}`,
      payload,
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );

    console.log(`Received response from Gemini AI API: ${response.status}`);

    if (response.status !== 200) {
      return res.status(500)
      .json({
        success: false,
        error: {
          code: ErrorCode.GEMINI_API_GENERIC_ERROR,
          message: "There was an error generating the chat response. Please try again!",
          message_title: "Internal Server Error",
        },
      });
    }

    console.log('Response data:', response.data);

    // Extract response content
    const candidates = response.data?.candidates || [];
    const contentText = candidates[0]?.content?.parts[0]?.text || 'No response received from the model.';

    // Respond with mapped chat API response
    return res.status(200)
    .json({
      success: true,
      data: {
        message: contentText,
        created_time: Date.now(),
      },
    });
  } catch (error) {
    console.error('Error generating chat response:', error);

    return res.status(500)
    .json({
      success: false,
      error: {
        code: ErrorCode.GEMINI_API_GENERIC_ERROR,
        message: "There was an error generating the chat response. Please try again!",
        message_title: "Internal Server Error",
      },
    });
  }
};

module.exports = {  
  generateChat
}
