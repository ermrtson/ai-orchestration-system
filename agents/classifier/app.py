from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

CLASSIFIER_PROMPT = """
Based on the summary below, assign appropriate tags to categorize this document. Choose from the following categories, but only include tags that clearly apply to the content:

- #methodology (if it focuses on research methods or approaches)
- #theory (if it discusses theoretical frameworks or concepts)
- #empirical (if it contains data analysis or experimental results)
- #case_study (if it examines specific instances or examples)
- #review (if it's a literature review or survey)
- #technical (if it involves technical implementation details)
- #qualitative (if it uses qualitative research methods)
- #quantitative (if it uses quantitative research methods)
- #ai (if it involves artificial intelligence)
- #ml (if it discusses machine learning)
- #nlp (if it's about natural language processing)
- #computing (if it's about computing systems or hardware)
- #social (if it addresses social aspects or implications)
- #education (if it's related to education or learning)
- #business (if it covers business or economic topics)
- #healthcare (if it's related to medicine or healthcare)

Summary:
{text}

Return your response as a JSON array of tags only, for example:
{{"tags": ["#methodology", "#empirical", "#quantitative"]}}
"""

class ClassifierRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify_text(request: ClassifierRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    text = request.text
    
    try:
        prompt = CLASSIFIER_PROMPT.format(text=text)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a text classification specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        response_text = response.choices[0].message.content
        
        # Extract the JSON part from the response
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Fallback with empty tags
            result = {"tags": []}
        
        return result
    
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    if not OPENAI_API_KEY:
        return {"status": "warning", "message": "API key not configured"}
    return {"status": "healthy"}