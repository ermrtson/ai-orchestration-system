from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set in environment variables")
else:
    openai.api_key = OPENAI_API_KEY

CITATION_PROMPT = """
Extract the bibliographic information from the following document. If the text is a research paper or article, look for the title, authors, year, journal, DOI, and other citation information.

If you can't find explicit citation information, try to infer as much as possible from the content (for example, author names mentioned, title at the top, dates, etc.).

Text:
{text}

Return the citation information in the following JSON format:
{
  "title": "Document title",
  "authors": "List of authors (comma-separated)",
  "year": "Publication year (YYYY)",
  "journal": "Journal or publication name",
  "doi": "DOI if available",
  "url": "URL if available"
}

If any field is not found, use null for that field.
"""

class CitationRequest(BaseModel):
    text: str
    filename: Optional[str] = None

@app.post("/extract")
async def extract_citation(request: CitationRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    # Use just the first portion of text for citation extraction
    # (usually citation info is at the beginning or end)
    text_sample = request.text[:10000]
    if len(request.text) > 10000:
        text_sample += "...\n\n" + request.text[-5000:]
    
    try:
        prompt = CITATION_PROMPT.format(text=text_sample)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a citation extraction specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content
        
        # Extract the JSON part from the response
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            
            # If we have a filename but no title was extracted, use filename as fallback
            if (not result.get("title") or result["title"] == "null") and request.filename:
                result["title"] = os.path.splitext(request.filename)[0].replace("_", " ").title()
                
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Fallback to basic info
            result = {
                "title": os.path.splitext(request.filename)[0].replace("_", " ").title() if request.filename else "Unknown Title",
                "authors": "Unknown",
                "year": "Unknown",
                "journal": "Unknown",
                "doi": None,
                "url": None
            }
        
        return result
    
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    if not OPENAI_API_KEY:
        return {"status": "warning", "message": "API key not configured"}
    return {"status": "healthy"}