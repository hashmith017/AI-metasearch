# AI Metasearch

A powerful web application that combines multiple AI models (Gemini and Groq) to provide comprehensive responses to queries, with support for multimodal inputs including text, images, and voice.

## Features

- **Multiple AI Models**: Leverages both Gemini and Groq APIs for comprehensive responses
- **Multimodal Input Support**:
  - Text-based queries
  - Image analysis (using Gemini Vision)
  - Voice input with speech-to-text conversion
- **Real-time Response Comparison**: Option to compare responses from different AI models
- **Interactive UI**: Clean and user-friendly interface with response cards
- **Copy Functionality**: Easy one-click copying of AI responses
- **Response Metrics**: View processing time and token usage information

## Setup

### Prerequisites

- Python 3.x
- Node.js and npm (for frontend development)
- API Keys:
  - Gemini API key
  - Groq API key

### Installation

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd AI-Metasearch
   ```

2. Create and configure the environment variables:
   ```bash
   # Create a .env file in the root directory
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

3. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn python-dotenv httpx python-multipart
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Usage

1. **Text Queries**:
   - Type your question in the input field
   - Click "Ask" or press Enter

2. **Image Analysis**:
   - Click the image upload button
   - Select an image file
   - Type your question about the image
   - Click "Ask"

3. **Voice Input**:
   - Click the microphone button
   - Speak your question
   - The query will be automatically submitted

4. **Compare Responses**:
   - Toggle the comparison button before asking your question
   - View side-by-side responses from different models

## Project Structure

```
AI-Metasearch/
├── main.py              # FastAPI backend server
├── static/
│   ├── app.js          # Frontend JavaScript
│   └── styles.css      # CSS styles
├── uploads/            # Temporary file storage
└── index.html          # Main frontend page
```

## Technical Details

- **Backend**: FastAPI (Python)
- **Frontend**: JavaScript, HTML, CSS
- **APIs**: 
  - Gemini API (for text and image analysis)
  - Groq API (for text analysis)
- **Features**:
  - Asynchronous API calls
  - Error handling and retry mechanisms
  - Real-time speech recognition
  - File upload handling
  - Base64 image encoding

## Error Handling

The application includes comprehensive error handling for:
- API failures
- Network issues
- Invalid file types
- Missing API keys
- Speech recognition errors

## Contributing

Feel free to submit issues and enhancement requests!
