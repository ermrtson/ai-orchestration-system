from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client (would be used in production)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ClassifierRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify_text(request: ClassifierRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    # For testing, return mock tags without calling OpenAI API
    return {
        "tags": ["#ai", "#ml", "#nlp", "#research", "#technical"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API key will be required in production"}

@app.get("/")
async def root():
    return {"message": "Classifier Agent ready"}