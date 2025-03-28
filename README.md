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

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│             │     │              │     │                 │
│  Frontend   │────▶│  MCP Server  │────▶│  Celery Worker  │
│             │     │              │     │                 │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                      Specialized AI Agents                         │
│                                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │             │  │             │  │             │  │           │ │
│  │File Handler │  │ Summarizer  │  │  Citation   │  │Classifier │ │
│  │             │  │  (Claude)   │  │    (GPT)    │  │   (GPT)   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘ │
│                                                                    │
│                           ┌─────────────┐                          │
│                           │             │                          │
│                           │   Quality   │                          │
│                           │    Check    │                          │
│                           │             │                          │
│                           └─────────────┘                          │
└────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │                  │
                         │   PostgreSQL     │
                         │   Database      │
                         │                  │
                         └──────────────────┘
```

The system uses a microservices architecture with:
- FastAPI for REST API endpoints
- PostgreSQL for data storage
- Celery for background task processing
- Redis for message brokering
- Docker for containerization and deployment

## Prerequisites

Before you begin, you'll need:

1. **Docker Desktop (REQUIRED)**
   - **IMPORTANT**: Docker Desktop must be installed and RUNNING
   - Windows/Mac: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: Install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

2. **API Keys**
   - [OpenAI API Key](https://platform.openai.com/)
   - [Anthropic API Key](https://www.anthropic.com/) for Claude

3. **Git** for cloning this repository

## Quick Start

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

1. **Make sure Docker Desktop is running**
   - Open Docker Desktop from your Applications folder (macOS) or Start Menu (Windows)
   - Wait for Docker to fully start (the whale icon should be solid, not animated)

2. **Clone the repository**
   ```bash
   git clone https://github.com/ermrtson/ai-orchestration-system.git
   cd ai-orchestration-system
   ```

3. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. **Edit the .env file** to add your API keys:
   ```bash
   # Open .env in your favorite editor
   nano .env
   
   # Add your API keys (no quotes or backticks)
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. **Start the system**
   ```bash
   docker-compose up -d
   ```

6. **Access the frontend**
   
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

| Agent | Description | Model |
|-------|-------------|-------|
| **File Handler** | Processes document files and splits them into chunks | N/A |
| **Summarizer** | Generates document summaries | Claude (Anthropic) |
| **Citation Extractor** | Extracts bibliographic information | GPT-4 (OpenAI) |
| **Classifier** | Tags documents with relevant categories | GPT-4 (OpenAI) |
| **Quality Checker** | Validates the output of all other agents | GPT-4 (OpenAI) |

### 3. Frontend

A React-based interface that allows users to:
- Upload documents
- View processing status
- Browse processed documents
- Search the document database

## Troubleshooting

If you encounter any issues, try our troubleshooting script:

```bash
chmod +x check_system.sh
./check_system.sh
```

Common issues:
- **Docker not running**: Make sure Docker Desktop is running (see [INSTALL.md](INSTALL.md))
- **API key format issues**: Ensure your .env file is properly formatted (no quotes or backticks)
- **Port conflicts**: Make sure ports 3000, 5432, 6379, and 8000-8005 are available

For more troubleshooting tips, see [INSTALL.md](INSTALL.md).

## Development

To modify or extend the system:

1. **Modify agent prompts**
   - Each agent has a prompt template you can modify in its `app.py` file

2. **Add new agents**
   - Create a new directory in the `agents/` folder
   - Follow the pattern of existing agents

3. **Modify the workflow**
   - Edit the document processing logic in `mcp/celery_app.py`

## API Endpoints

The MCP Server provides the following API endpoints:

- `GET /`: Welcome message
- `POST /upload/`: Upload a document for processing
- `GET /task/{task_id}`: Get the status of a processing task
- `GET /document/{document_id}`: Get details of a processed document
- `GET /documents/`: Get a list of all processed documents

## Next Steps

After implementing the basic system, consider these enhancements:

1. Adding document vector embeddings for semantic search
2. Implementing user authentication
3. Adding more LLM providers (Llama, Mixtral, etc.)
4. Implementing real-time progress updates via WebSockets
5. Creating advanced visualization of document relationships

## License

MIT License - See LICENSE file for details