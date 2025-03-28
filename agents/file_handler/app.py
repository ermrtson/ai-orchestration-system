from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    max_length: Optional[int] = 8000

class ChunkResponse(BaseModel):
    chunks: List[str]

@app.post("/chunk", response_model=ChunkResponse)
async def chunk_text(request: TextRequest):
    """Split text into manageable chunks"""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text = request.text
    max_length = request.max_length
    
    # Simple chunking strategy
    if len(text) <= max_length:
        return {"chunks": [text]}
    
    chunks = []
    current_chunk = ""
    
    for paragraph in text.split("\n\n"):
        if len(current_chunk) + len(paragraph) + 2 <= max_length:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return {"chunks": chunks}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "File Handler Agent ready"}