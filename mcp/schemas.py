from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TaskResponse(BaseModel):
    task_id: str
    status: str

class TaskDetails(BaseModel):
    task_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    document_id: Optional[str] = None

class DocumentDetails(BaseModel):
    id: str
    title: Optional[str] = None
    summary: Optional[str] = None
    citation: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = []
    created_at: datetime

class SearchQuery(BaseModel):
    text: str
    limit: int = 5

class SearchResult(BaseModel):
    id: str
    title: str
    similarity: float