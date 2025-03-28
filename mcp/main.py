from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import uuid
from datetime import datetime
from typing import List

# Initialize FastAPI
app = FastAPI(title="LLM Orchestrator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to LLM Orchestrator API"}

@app.post("/upload/")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    # Generate a unique ID for this task
    task_id = str(uuid.uuid4())
    
    # Save the uploaded file
    file_path = f"uploads/{task_id}_{file.filename}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Return a response immediately (demo mode)
    return {"task_id": task_id, "status": "Processing started"}

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    # In demo mode, always return completed
    return {
        "task_id": task_id,
        "status": "COMPLETED",
        "created_at": datetime.now().isoformat(),
        "completed_at": datetime.now().isoformat(),
        "document_id": "123"  # Demo document ID
    }

@app.get("/document/{document_id}")
def get_document(document_id: str):
    # For demo purposes, return a static document
    if document_id == "123":
        return {
            "id": "123",
            "title": "Advanced NLP Techniques",
            "summary": "This paper explores cutting-edge natural language processing methods including transformer architectures and their applications in various domains.",
            "citation": json.dumps({
                "title": "Advanced NLP Techniques",
                "authors": "Jane Smith, John Doe",
                "year": "2025",
                "journal": "Journal of AI Research",
                "doi": "10.1234/jair.5678",
                "url": "https://example.com/papers/nlp-techniques"
            }),
            "tags": "#nlp,#ai,#research",
            "created_at": datetime.now().isoformat()
        }
    elif document_id == "456":
        return {
            "id": "456",
            "title": "Machine Learning in Healthcare",
            "summary": "A comprehensive study on applying machine learning algorithms to healthcare data, focusing on early disease detection and personalized medicine.",
            "citation": json.dumps({
                "title": "Machine Learning in Healthcare",
                "authors": "Alex Johnson, Maria Garcia",
                "year": "2025",
                "journal": "Healthcare Informatics",
                "doi": "10.5678/health.1234",
                "url": "https://example.com/papers/ml-healthcare"
            }),
            "tags": "#ml,#healthcare,#research",
            "created_at": datetime.now().isoformat()
        }
    else:
        raise HTTPException(status_code=404, detail="Document not found")

@app.get("/documents/")
def get_all_documents():
    # For demo purposes, return static documents
    return [
        {
            "id": "123",
            "title": "Advanced NLP Techniques",
            "summary": "This paper explores cutting-edge natural language processing methods including transformer architectures and their applications in various domains.",
            "citation": json.dumps({
                "title": "Advanced NLP Techniques",
                "authors": "Jane Smith, John Doe",
                "year": "2025",
                "journal": "Journal of AI Research",
                "doi": "10.1234/jair.5678",
                "url": "https://example.com/papers/nlp-techniques"
            }),
            "tags": "#nlp,#ai,#research",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "456",
            "title": "Machine Learning in Healthcare",
            "summary": "A comprehensive study on applying machine learning algorithms to healthcare data, focusing on early disease detection and personalized medicine.",
            "citation": json.dumps({
                "title": "Machine Learning in Healthcare",
                "authors": "Alex Johnson, Maria Garcia",
                "year": "2025",
                "journal": "Healthcare Informatics",
                "doi": "10.5678/health.1234",
                "url": "https://example.com/papers/ml-healthcare"
            }),
            "tags": "#ml,#healthcare,#research",
            "created_at": datetime.now().isoformat()
        }
    ]