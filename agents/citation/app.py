from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client (would be used in production)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CitationRequest(BaseModel):
    text: str
    filename: Optional[str] = None

@app.post("/extract")
async def extract_citation(request: CitationRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    # For testing, return mock citation data without calling OpenAI API
    filename = request.filename or "Unknown Document"
    return {
        "title": filename.replace(".pdf", "").replace(".txt", "").replace("_", " ").title(),
        "authors": "John Doe, Jane Smith",
        "year": "2025",
        "journal": "Journal of Advanced AI Systems",
        "doi": "10.1234/example.5678",
        "url": "https://example.com/paper"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API key will be required in production"}

@app.get("/")
async def root():
    return {"message": "Citation Agent ready"}