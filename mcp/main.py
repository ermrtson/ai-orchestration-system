from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import uuid
from datetime import datetime
from models import Task, Agent, Document
from database import SessionLocal, engine, Base
from celery_app import process_document
import schemas
from typing import List
from dotenv import load_dotenv

load_dotenv()

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

# Create DB tables
Base.metadata.create_all(bind=engine)

# Make sure uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to LLM Orchestrator API"}

@app.post("/upload/", response_model=schemas.TaskResponse)
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
    
    # Store task in database
    db = SessionLocal()
    try:
        new_task = Task(
            id=task_id,
            file_name=file.filename,
            file_path=file_path,
            status="PENDING",
            created_at=datetime.now()
        )
        db.add(new_task)
        db.commit()
    finally:
        db.close()
    
    # Process the file asynchronously
    background_tasks.add_task(
        lambda: process_document.delay(task_id, file_path)
    )
    
    return {"task_id": task_id, "status": "Processing started"}

@app.get("/task/{task_id}", response_model=schemas.TaskDetails)
def get_task_status(task_id: str):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "task_id": task.id,
            "status": task.status,
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "document_id": task.document_id
        }
    finally:
        db.close()

@app.get("/document/{document_id}", response_model=schemas.DocumentDetails)
def get_document(document_id: str):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": document.id,
            "title": document.title,
            "summary": document.summary,
            "citation": json.loads(document.citation) if document.citation else None,
            "tags": document.tags.split(",") if document.tags else [],
            "created_at": document.created_at
        }
    finally:
        db.close()

@app.get("/documents/", response_model=List[schemas.DocumentDetails])
def get_all_documents():
    db = SessionLocal()
    try:
        documents = db.query(Document).order_by(Document.created_at.desc()).all()
        
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "summary": doc.summary,
                "citation": json.loads(doc.citation) if doc.citation else None,
                "tags": doc.tags.split(",") if doc.tags else [],
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    finally:
        db.close()