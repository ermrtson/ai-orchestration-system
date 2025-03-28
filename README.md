# AI Orchestration System

A comprehensive multi-agent LLM orchestration system for processing documents - from zero to a fully functional system.

## Overview

This project creates a complete document processing pipeline using multiple AI agents, each specialized in different tasks:

- **MCP (Master Control Program)**: Coordinates the workflow between agents
- **File Handler**: Processes documents and splits them into manageable chunks
- **Summarizer (Claude)**: Creates concise summaries of documents
- **Citation Extractor (GPT)**: Extracts bibliographic information
- **Classifier (GPT)**: Tags documents with relevant categories
- **Quality Checker**: Validates the output from all agents

## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400?text=AI+Orchestration+System+Architecture)

The system uses a microservices architecture with:
- FastAPI for REST API endpoints
- PostgreSQL for data storage
- Celery for background task processing
- Redis for message brokering
- Docker for containerization and deployment

## Prerequisites

Before you begin, you'll need:

1. **Docker & Docker Compose**
   - Windows/Mac: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: Install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

2. **API Keys**
   - [OpenAI API Key](https://platform.openai.com/)
   - [Anthropic API Key](https://www.anthropic.com/) for Claude

3. **Git** for cloning this repository

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ermrtson/ai-orchestration-system.git
   cd ai-orchestration-system
   ```

2. **Create a .env file in the root directory**
   ```bash
   # Create and edit .env file
   cat > .env << 'EOF'
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   DATABASE_URL=postgresql://llmuser:llmpassword@postgres/llmorchestrator
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   EOF
   ```

3. **Start the system**
   ```bash
   docker-compose up -d
   ```

4. **Access the frontend**
   
   Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## System Components

### 1. MCP (Master Control Program)

The central orchestrator that:
- Receives document uploads
- Distributes processing tasks to specialized agents
- Tracks document processing status
- Stores processed documents in the database
- Provides API endpoints for the frontend

### 2. Specialized AI Agents

Each agent is implemented as a separate microservice:

- **File Handler**: Processes document files and splits them into chunks
- **Summarizer**: Uses Claude to generate document summaries
- **Citation Extractor**: Uses GPT to extract bibliographic information
- **Classifier**: Uses GPT to tag documents with relevant categories
- **Quality Checker**: Validates the output of all other agents

### 3. Frontend

A simple React-based interface that allows users to:
- Upload documents
- View processing status
- Browse processed documents
- Search the document database

## Development

To modify or extend the system:

1. **Modify agent prompts**
   - Each agent has a prompt template you can modify in its `app.py` file

2. **Add new agents**
   - Create a new directory in the `agents/` folder
   - Follow the pattern of existing agents

3. **Modify the workflow**
   - Edit the document processing logic in `mcp/celery_app.py`

## Troubleshooting

- **Check service status**: `docker-compose ps`
- **View logs**: `docker-compose logs mcp` (or any other service name)
- **Restart a service**: `docker-compose restart mcp` (or any other service name)
- **Reset the entire system**: `docker-compose down -v && docker-compose up -d`

## Next Steps

After implementing the basic system, consider these enhancements:

1. Adding document vector embeddings for semantic search
2. Implementing user authentication
3. Adding more LLM providers (Llama, Mixtral, etc.)
4. Implementing real-time progress updates via WebSockets
5. Creating advanced visualization of document relationships

## License

MIT License - See LICENSE file for details
