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
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```
<img width="1097" height="248" alt="image" src="https://github.com/user-attachments/assets/e4bf28ba-f21c-40e8-a37f-9714c1fb851c" />

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

<img width="1919" height="998" alt="image" src="https://github.com/user-attachments/assets/414ee758-dce6-4b44-a11e-1f5671f63b65" />

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
    
**Example 1:**
<img width="1431" height="850" alt="image" src="https://github.com/user-attachments/assets/7b02c8b0-8600-45ee-b535-6782f5e6e100" />
<img width="1410" height="695" alt="image" src="https://github.com/user-attachments/assets/53bb10a7-5657-49b7-a038-c79e4a96765d" />

**Example 2:**
<img width="1919" height="992" alt="image" src="https://github.com/user-attachments/assets/12199781-e330-44d8-ad4a-d73d0285d9fd" />
<img width="1397" height="681" alt="image" src="https://github.com/user-attachments/assets/169977f4-4c07-4a2b-ba02-b6103ebc2bf7" />

## Error Handling

The application includes comprehensive error handling for:
- API failures
- Network issues
- Invalid file types
- Missing API keys
- Speech recognition errors

## Contributing

Feel free to submit issues and enhancement requests!

