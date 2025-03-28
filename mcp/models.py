from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, nullable=False)  # PENDING, PROCESSING, COMPLETED, FAILED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    
    document = relationship("Document", back_populates="task")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    citation = Column(Text, nullable=True)  # JSON string
    tags = Column(String, nullable=True)    # Comma-separated tags
    vector_embedding = Column(Text, nullable=True)  # JSON string of embedding
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    task = relationship("Task", back_populates="document")

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # FILE_HANDLER, SUMMARIZER, etc.
    llm_provider = Column(String, nullable=False)  # CLAUDE, GPT, GLAMA, etc.
    prompt_template = Column(Text, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)