from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import os
import base64
import httpx
import logging
from logging.config import dictConfig

# Configure logging
dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s:     %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr"
        }
    },
    "loggers": {
        "app_logger": {
            "handlers": ["default"],
            "level": "DEBUG"
        }
    }
})
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Data Models
class Query(BaseModel):
    question: str
    images: Optional[List[str]] = None
    pdf: Optional[str] = None
    voice: Optional[str] = None
    compare: Optional[bool] = False

class AIResponse(BaseModel):
    model: str
    response: str
    tokens: Optional[int] = None
    processing_time: Optional[float] = None

# Initialize FastAPI app
app = FastAPI(title="AI Metasearch")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def read_root():
    return FileResponse(
        "index.html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logger = logging.getLogger("app_logger")

async def ask_groq(question: str, context: str = "") -> AIResponse:
    """
    Query the Groq API with error handling and response formatting
    """
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Groq API key not found")
    
    start_time = datetime.now()
    try:
        full_prompt = f"{context}\n\n{question}" if context else question
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": full_prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if "choices" not in data or not data["choices"]:
                raise HTTPException(status_code=500, detail="No response from Groq")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AIResponse(
                model="groq",
                response=data["choices"][0]["message"]["content"],
                tokens=data.get("usage", {}).get("total_tokens"),
                processing_time=processing_time
            )
            
    except httpx.HTTPError as e:
        error_msg = f"Groq API Error: {str(e)}"
        if response := getattr(e, 'response', None):
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg = f"Groq API Error: {error_data['error'].get('message', str(e))}"
            except:
                pass
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def ask_gemini(question: str, image_data: Optional[str] = None):
    """
    Query the Gemini API with error handling and response formatting
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not found")
    
    start_time = datetime.now()
    try:
        async with httpx.AsyncClient() as client:
            # Prepare request body
            request_body = {
                "contents": [{
                    "parts":[{
                        "text": question
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2000,
                    "topP": 0.8,
                    "topK": 400
                }
            }

            # Add image if provided
            if image_data:
                request_body["contents"][0]["parts"].append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_data
                    }
                })

            response = await client.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                headers={
                    "Content-Type": "application/json",
                    "X-goog-api-key": GEMINI_API_KEY
                },
                json=request_body,
                timeout=30.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "candidates" in data and len(data["candidates"]) > 0:
                processing_time = (datetime.now() - start_time).total_seconds()
                return AIResponse(
                    model="gemini",
                    response=data["candidates"][0]["content"]["parts"][0]["text"],
                    tokens=None,  # Gemini doesn't provide token count
                    processing_time=processing_time
                )
            raise HTTPException(status_code=500, detail="No response from Gemini")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/ask")
async def ask_all(
    question: str = Form(...),
    compare: bool = Form(default=False),
    files: Optional[List[UploadFile]] = File(None)
):
    try:
        print(f"Received question: {question}")
        
        # Process uploaded files if any
        image_data = None
        if files:
            for file in files:
                if file.content_type.startswith('image/'):
                    contents = await file.read()
                    image_data = base64.b64encode(contents).decode('utf-8')
                    break  # Process only first image for now
        
        # Create and await tasks for both APIs
        tasks = [
            asyncio.create_task(ask_gemini(question, image_data)),
            asyncio.create_task(ask_groq(question))
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Format responses with detailed error handling
        response = {
            "gemini": results[0] if isinstance(results[0], AIResponse) else str(results[0]),
            "groq": results[1] if isinstance(results[1], AIResponse) else str(results[1])
        }
        
        return response
        
    except Exception as e:
        print(f"Error in ask_all: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
