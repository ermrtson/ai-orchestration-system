#!/bin/bash

# AI Orchestration System Checker

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==== AI Orchestration System Status Checker ====${NC}"

# Check Docker installation
echo -e "\n${YELLOW}Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
else
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}Docker is installed: ${DOCKER_VERSION}${NC}"
fi

# Check Docker Compose installation
echo -e "\n${YELLOW}Checking Docker Compose installation...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Warning: Docker Compose command not found.${NC}"
    echo "Note: Docker Compose might be integrated into Docker CLI in newer versions."
else
    COMPOSE_VERSION=$(docker-compose --version)
    echo -e "${GREEN}Docker Compose is installed: ${COMPOSE_VERSION}${NC}"
fi

# Check if Docker daemon is running
echo -e "\n${YELLOW}Checking if Docker daemon is running...${NC}"
if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker daemon is not running.${NC}"
    echo -e "${YELLOW}Please start Docker Desktop first and try again.${NC}"
    echo "If using macOS, please open Docker Desktop from your Applications folder."
    echo "Wait for Docker to fully start (solid whale icon in menu bar) before continuing."
    exit 1
else
    echo -e "${GREEN}Docker daemon is running!${NC}"
fi

# Check .env file
echo -e "\n${YELLOW}Checking .env file...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found.${NC}"
    echo "Please run ./setup.sh to create the .env file."
    exit 1
fi

# Check if API keys are properly set
echo -e "\n${YELLOW}Checking API keys in .env file...${NC}"
if grep -q "your_openai_api_key_here\|your_anthropic_api_key_here" .env; then
    echo -e "${RED}Warning: API keys are not properly set in .env file.${NC}"
    echo "Would you like to edit the .env file now? (y/n)"
    read -r edit_env
    if [[ $edit_env == "y" || $edit_env == "Y" ]]; then
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo "Please edit the .env file manually with your preferred text editor."
        fi
    fi
else
    echo -e "${GREEN}API keys seem to be set in .env file.${NC}"
fi

# Check running containers
echo -e "\n${YELLOW}Checking running containers...${NC}"
if docker-compose ps &> /dev/null; then
    RUNNING_CONTAINERS=$(docker-compose ps -q | wc -l)
    if [ "$RUNNING_CONTAINERS" -eq 0 ]; then
        echo -e "${RED}No containers are running.${NC}"
        echo "Would you like to start the system now? (y/n)"
        read -r start_system
        if [[ $start_system == "y" || $start_system == "Y" ]]; then
            docker-compose up -d
        fi
    else
        echo -e "${GREEN}${RUNNING_CONTAINERS} containers are running.${NC}"
        docker-compose ps
    fi
else
    echo -e "${RED}Error running docker-compose command.${NC}"
    echo "Please make sure you are in the project directory."
fi

echo -e "\n${BLUE}==== Status Check Complete ====${NC}"
echo "For more detailed installation instructions, see INSTALL.md"
