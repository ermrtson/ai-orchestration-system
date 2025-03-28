#!/bin/bash

# AI Orchestration System Setup Script

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==== AI Orchestration System Setup ====${NC}"
echo "This script will set up the AI Orchestration System."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker daemon is not running.${NC}"
    echo -e "${YELLOW}Please start Docker Desktop first and try again.${NC}"
    echo "If using macOS, please open Docker Desktop from your Applications folder."
    echo "Wait for Docker to fully start (solid whale icon in menu bar) before continuing."
    exit 1
fi

# Create required directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p mcp/uploads
mkdir -p agents/file_handler
mkdir -p agents/summarizer
mkdir -p agents/citation
mkdir -p agents/classifier
mkdir -p agents/quality
mkdir -p frontend
mkdir -p uploads

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << 'EOF'
# OpenAI API Key for GPT services (required for citation, classifier, and quality agents)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DATABASE_URL=postgresql://llmuser:llmpassword@postgres/llmorchestrator
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF
    echo -e "${YELLOW}Please edit the .env file to add your API keys.${NC}"
    echo -e "${YELLOW}Open the .env file in a text editor and replace the placeholder API keys with your actual keys.${NC}"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

# Check if API keys are set in .env
if grep -q "your_openai_api_key_here\|your_anthropic_api_key_here" .env; then
    echo -e "${RED}Warning: API keys are not set in .env file.${NC}"
    echo "Please set your OpenAI and Anthropic API keys in the .env file before running the system."
    echo "For demo mode, you can continue without API keys, but some features will be limited."
fi

# Pull necessary Docker images
echo -e "${YELLOW}Pulling necessary Docker images...${NC}"
docker pull postgres:14-alpine
docker pull redis:7-alpine
docker pull node:18-alpine
docker pull python:3.10-slim

# Verify that all required files exist
echo -e "${YELLOW}Checking for required files...${NC}"
missing_files=false

# Check Dockerfiles
for dir in mcp agents/file_handler agents/summarizer agents/citation agents/classifier agents/quality frontend; do
    if [ ! -f "$dir/Dockerfile" ]; then
        echo -e "${RED}Missing: $dir/Dockerfile${NC}"
        missing_files=true
    fi
done

# Check requirements files
for dir in mcp agents/file_handler agents/summarizer agents/citation agents/classifier agents/quality; do
    if [ ! -f "$dir/requirements.txt" ]; then
        echo -e "${RED}Missing: $dir/requirements.txt${NC}"
        missing_files=true
    fi
done

# Check frontend package.json
if [ ! -f "frontend/package.json" ]; then
    echo -e "${RED}Missing: frontend/package.json${NC}"
    missing_files=true
fi

# Check main application files
if [ ! -f "mcp/main.py" ]; then
    echo -e "${RED}Missing: mcp/main.py${NC}"
    missing_files=true
fi

for dir in agents/file_handler agents/summarizer agents/citation agents/classifier agents/quality; do
    if [ ! -f "$dir/app.py" ]; then
        echo -e "${RED}Missing: $dir/app.py${NC}"
        missing_files=true
    fi
done

if [ "$missing_files" = true ]; then
    echo -e "${RED}Some required files are missing. Please run 'git pull' to update your repository.${NC}"
    exit 1
fi

# Start the system
echo -e "${YELLOW}Starting AI Orchestration System...${NC}"
docker-compose up -d

# Check if all services are running
sleep 5
services=$(docker-compose ps -q | wc -l)
if [ "$services" -lt 9 ]; then
    echo -e "${RED}Warning: Some services might not be running.${NC}"
    echo "Check the status with: docker-compose ps"
    echo "View logs with: docker-compose logs -f"
else
    echo -e "${GREEN}All services are running!${NC}"
fi

echo -e "${GREEN}==== Setup Complete ====${NC}"
echo "You can access the frontend at: http://localhost:3000"
echo "The API is available at: http://localhost:8000"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop system: docker-compose down"
echo "  - Restart system: docker-compose restart"
echo "  - Check system status: ./check_system.sh"
