# Installation Guide for AI Orchestration System

This guide provides detailed step-by-step instructions for setting up the AI Orchestration System on your machine.

## Prerequisites

### 1. Install Docker Desktop

#### macOS:
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Double-click the downloaded `.dmg` file and drag Docker to the Applications folder
3. **IMPORTANT**: Open Docker Desktop from your Applications folder
4. Wait for Docker to fully start (the whale icon in the menu bar should be solid, not animated)
5. Verify Docker is running with `docker ps` in Terminal

#### Windows:
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer and follow the instructions
3. **IMPORTANT**: Start Docker Desktop after installation
4. Wait for Docker to fully start
5. Verify Docker is running with `docker ps` in Command Prompt or PowerShell

#### Linux:
1. Install Docker Engine using the [official instructions](https://docs.docker.com/engine/install/)
2. Install Docker Compose using the [official instructions](https://docs.docker.com/compose/install/)
3. Start Docker: `sudo systemctl start docker`
4. Verify Docker is running: `docker ps`

### 2. Obtain API Keys

#### OpenAI API Key:
1. Go to [OpenAI's platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API keys section
4. Create a new API key and copy it

#### Anthropic API Key:
1. Go to [Anthropic's website](https://www.anthropic.com/)
2. Sign up for Claude API access
3. Once approved, obtain your API key from the dashboard

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ermrtson/ai-orchestration-system.git
cd ai-orchestration-system
```

### 2. Make Sure Docker is Running

Before proceeding, ensure Docker Desktop is running:

- **macOS/Windows**: Look for the Docker whale icon in the menu bar/system tray
- **Linux**: Run `sudo systemctl status docker` to check if Docker is active

### 3. Run the Setup Script

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:
- Check if Docker is running
- Create necessary directories
- Create a default `.env` file
- Start the system using Docker Compose

### 4. Configure API Keys

After running the setup script, you need to edit the `.env` file to add your API keys:

```bash
# Edit the .env file with your preferred text editor
nano .env
```

Replace the placeholders with your actual API keys:

```
OPENAI_API_KEY=your_actual_openai_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_key_here
```

**IMPORTANT**: Do not include any special characters (like backticks) around your API keys.

### 5. Restart the System

After updating your API keys, restart the system:

```bash
docker-compose down
docker-compose up -d
```

### 6. Access the System

- Frontend interface: [http://localhost:3000](http://localhost:3000)
- API endpoint: [http://localhost:8000](http://localhost:8000)

## Troubleshooting

### Docker Daemon Not Running

If you see an error like:
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

**Solution**:
- **macOS/Windows**: Open Docker Desktop from Applications/Start Menu
- **Linux**: Start Docker with `sudo systemctl start docker`

### API Key Format Issues

If you see errors related to `.env` file parsing:

**Solution**:
- Make sure your API keys don't have quotes, backticks, or special characters around them
- The format should be `KEY=value` with no spaces around the `=` sign

### Containers Not Starting

If some containers fail to start:

**Solution**:
1. Check Docker logs: `docker-compose logs -f`
2. Ensure all directories are created: `mkdir -p mcp/uploads agents/file_handler agents/summarizer agents/citation agents/classifier agents/quality frontend`
3. Rebuild containers: `docker-compose build`
4. Restart: `docker-compose up -d`

### Resource Limitations

If Docker crashes or containers fail to start due to resource constraints:

**Solution**:
- Open Docker Desktop settings
- Increase CPU and memory allocations
- Restart Docker Desktop

## System Maintenance

### Stopping the System

```bash
docker-compose down
```

### Updating the System

```bash
git pull
docker-compose build
docker-compose up -d
```

### Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View logs for a specific service
docker-compose logs -f mcp
```

### Resetting the System

To completely reset the system (including the database):

```bash
docker-compose down -v
./setup.sh
```

## Need More Help?

If you encounter issues not covered in this guide, please:

1. Check the [GitHub repository issues](https://github.com/ermrtson/ai-orchestration-system/issues)
2. Submit a new issue with details about your problem
