from celery import Celery
import os
import requests
import json
import time
from database import SessionLocal
from models import Task, Document
import uuid
from datetime import datetime
import pypdf  # For PDF processing
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

@celery_app.task
def process_document(task_id, file_path):
    """
    Process a document through the AI agent pipeline
    """
    db = SessionLocal()
    try:
        # Update task status
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return {"error": "Task not found"}
        
        task.status = "PROCESSING"
        db.commit()
        
        # Determine file type and extract text
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            task.status = "FAILED"
            db.commit()
            return {"error": "Unsupported file type"}
        
        # Step 1: File handler processing (text extraction, chunking)
        chunks = chunk_text(text, max_length=8000)
        
        # Step 2: Summarization
        summary_response = requests.post(
            "http://summarizer:8000/summarize",
            json={"text": chunks[0] if len(chunks) == 1 else text}
        )
        
        if summary_response.status_code != 200:
            task.status = "FAILED"
            db.commit()
            return {"error": f"Summarizer failed: {summary_response.text}"}
        
        summary_data = summary_response.json()
        
        # Step 3: Citation extraction
        citation_response = requests.post(
            "http://citation:8000/extract",
            json={"text": text, "filename": os.path.basename(file_path)}
        )
        
        if citation_response.status_code != 200:
            citation_data = {}
        else:
            citation_data = citation_response.json()
        
        # Step 4: Classification
        classifier_response = requests.post(
            "http://classifier:8000/classify",
            json={"text": summary_data["summary"]}
        )
        
        if classifier_response.status_code != 200:
            tags = []
        else:
            tags = classifier_response.json().get("tags", [])
        
        # Step 5: Quality check
        quality_response = requests.post(
            "http://quality:8000/validate",
            json={
                "summary": summary_data,
                "citation": citation_data,
                "tags": tags
            }
        )
        
        if quality_response.status_code != 200:
            validation_result = {"is_valid": False, "errors": ["Quality check failed"]}
        else:
            validation_result = quality_response.json()
        
        # Step 6: Store document
        document_id = str(uuid.uuid4())
        document = Document(
            id=document_id,
            title=summary_data.get("title", ""),
            summary=summary_data.get("summary", ""),
            citation=json.dumps(citation_data),
            tags=",".join(tags),
            created_at=datetime.now()
        )
        
        db.add(document)
        
        # Update task
        task.status = "COMPLETED"
        task.completed_at = datetime.now()
        task.document_id = document_id
        
        db.commit()
        
        return {"document_id": document_id}
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        # Update task as failed
        try:
            task.status = "FAILED"
            db.commit()
        except:
            pass
        
        return {"error": str(e)}
    
    finally:
        db.close()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
    return text

def chunk_text(text, max_length=8000):
    """Split text into chunks of maximum length"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    for paragraph in text.split("\n\n"):
        if len(current_chunk) + len(paragraph) <= max_length:
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks