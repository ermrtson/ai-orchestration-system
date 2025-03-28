from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    logger.warning("ANTHROPIC_API_KEY not set in environment variables")

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SUMMARIZER_PROMPT = """
You are a precise scientific summarizer. Please summarize the following text in 3-5 paragraphs, focusing on:
1. Main research questions and objectives
2. Methodology used
3. Key findings
4. Limitations and future work

Text to summarize:
{text}

Return your response in the following JSON format:
{
  "title": "Extracted or inferred title",
  "summary": "Your 3-5 paragraph summary",
  "key_findings": ["Finding 1", "Finding 2", "..."]
}
"""

class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="Anthropic API key not configured")
    
    text = request.text
    
    try:
        prompt = SUMMARIZER_PROMPT.format(text=text)
        
        message = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Extract the JSON part from the response
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Attempt to fix common JSON issues
            result = {
                "title": "Parsing Error - Please check logs",
                "summary": response_text,
                "key_findings": []
            }
        
        return result
    
    except Exception as e:
        logger.error(f"Error calling Claude API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    if not ANTHROPIC_API_KEY:
        return {"status": "warning", "message": "API key not configured"}
    return {"status": "healthy"}