from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import openai
import os
import json
import logging
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

QUALITY_PROMPT = """
You are a quality assurance specialist for an AI document processing system. 
Please evaluate the following output from our document processing pipeline and check for any issues or inconsistencies.

Summary Data:
{summary}

Citation Data:
{citation}

Tags:
{tags}

Please check for the following issues:
1. Is the summary coherent and does it appear to accurately represent a document?
2. Does the citation information seem reasonable and properly formatted?
3. Do the tags seem appropriate for the type of content?
4. Are there any obvious errors or inconsistencies across these elements?

Return your assessment in the following JSON format:
{{
  "is_valid": true/false,
  "errors": ["Error 1", "Error 2"],
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}}
"""

class QualityRequest(BaseModel):
    summary: Dict[str, Any]
    citation: Dict[str, Any]
    tags: List[str]

class QualityResponse(BaseModel):
    is_valid: bool
    errors: List[str] = []
    suggestions: List[str] = []

@app.post("/validate", response_model=QualityResponse)
async def validate_document(request: QualityRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        # Format the inputs for the prompt
        summary_str = json.dumps(request.summary, indent=2)
        citation_str = json.dumps(request.citation, indent=2)
        tags_str = ", ".join(request.tags) if request.tags else "No tags provided"
        
        prompt = QUALITY_PROMPT.format(
            summary=summary_str,
            citation=citation_str,
            tags=tags_str
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a quality assurance specialist."},
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
            
            # Ensure we have all required fields
            if "is_valid" not in result:
                result["is_valid"] = False
            if "errors" not in result:
                result["errors"] = []
            if "suggestions" not in result:
                result["suggestions"] = []
                
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Fallback to basic response
            result = {
                "is_valid": True,  # Default to valid to not block processing
                "errors": ["Error parsing quality check response"],
                "suggestions": ["Review document manually"]
            }
        
        return result
    
    except Exception as e:
        logger.error(f"Error in quality validation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    if not OPENAI_API_KEY:
        return {"status": "warning", "message": "API key not configured"}
    return {"status": "healthy"}
