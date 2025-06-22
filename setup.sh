#!/bin/bash
# This script sets up the development environment for the Patient Care Coordination & Telemedicine Platform.

# Exit immediately if a command exits with a non-zero status.
set -e

# Helper to log messages
log() {
    echo "[setup] $1"
}

# --- System Dependency Installation ---

log "Detecting operating system and package manager..."
OS_NAME="$(uname -s)"
PKG_MANAGER=""
INSTALL_CMD=""
UPDATE_CMD=""
PACKAGES=()

# Detect package manager
if command -v brew > /dev/null; then
    PKG_MANAGER="brew"
    INSTALL_CMD="brew install"
    UPDATE_CMD="brew update"
    PACKAGES=(python@3 git node)
elif command -v apt-get > /dev/null; then
    PKG_MANAGER="apt-get"
    INSTALL_CMD="sudo apt-get install -y"
    UPDATE_CMD="sudo apt-get update"
    PACKAGES=(python3 python3-pip python3-venv git nodejs npm)
elif command -v yum > /dev/null; then
    PKG_MANAGER="yum"
    INSTALL_CMD="sudo yum install -y"
    UPDATE_CMD="sudo yum update -y"
    PACKAGES=(python3 python3-pip git nodejs)
elif command -v dnf > /dev/null; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
    UPDATE_CMD="sudo dnf update -y"
    PACKAGES=(python3 python3-pip git nodejs)
elif command -v pacman > /dev/null; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S --noconfirm"
    UPDATE_CMD="sudo pacman -Sy"
    PACKAGES=(python python-pip git nodejs npm)
elif command -v choco > /dev/null; then
    PKG_MANAGER="choco"
    INSTALL_CMD="choco install -y"
    UPDATE_CMD="choco upgrade -y"
    PACKAGES=(python git nodejs)
else
    log "Unsupported OS or package manager not found."
    exit 1
fi

log "Using $PKG_MANAGER to install dependencies."

# Update package lists
log "Updating package lists..."
$UPDATE_CMD

# Install required packages
log "Installing system packages: ${PACKAGES[*]}"
for pkg in "${PACKAGES[@]}"; do
    # Check if the primary command of the package is installed
    if ! command -v "${pkg%%@*}" >/dev/null; then
        log "Installing $pkg..."
        $INSTALL_CMD "$pkg"
    else
        log "$pkg is already installed."
    fi
done

# --- Python Backend Setup ---

log "Setting up Python virtual environment..."
if [ ! -d .venv ]; then
    python3 -m venv .venv
    log "Virtual environment created at ./.venv"
fi

# Activate virtual environment
source .venv/bin/activate

log "Upgrading pip..."
pip install --upgrade pip

# Create and install Python dependencies
if [ ! -f requirements.txt ]; then
    log "Creating requirements.txt..."
    cat <<EOF > requirements.txt
fastapi
uvicorn[standard]
python-dotenv
SQLAlchemy
# Add other Python dependencies here
EOF
fi

log "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# --- Node.js Frontend Setup ---

log "Setting up Node.js environment..."

# Create package.json if it doesn't exist
if [ ! -f package.json ]; then
    log "Creating package.json..."
    cat <<EOF > package.json
{
  "name": "health-project-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^4.9.5",
    "@mastra/core": "latest"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
EOF
fi

if command -v npm >/dev/null; then
    log "Installing Node.js dependencies..."
    npm install
else
    log "npm not found. Please install Node.js and npm."
fi


# --- Environment Configuration ---

log "Setting up environment variables..."
if [ ! -f .env.template ]; then
    log "Creating .env.template from data_config.md..."
    cat <<EOF > .env.template
# This file contains environment variables for the DEVELOPMENT environment.
# A .env.example file with the keys but not the values should be committed instead.

# Application Settings
NODE_ENV=development

# Database Configuration
# Using SQLite for simple, file-based local development.
# In production, this will point to a managed PostgreSQL or MySQL database.
DATABASE_URL=sqlite:///./healthcare_dev.db

# Security Settings
# IMPORTANT: This is a weak, predictable secret for development only.
# In production, this must be a long, randomly generated string stored securely.
JWT_SECRET=dev-secret-change-later-in-production

# AI Service API Keys
# Your key for the OpenAI API.
OPENAI_API_KEY=your-openai-api-key-goes-here

# Feature Flags for Incremental Development
# These flags allow us to turn features on or off without changing code.
# This is useful for gradually rolling out security enhancements.
ENCRYPTION_ENABLED=false
MFA_ENABLED=false
HIPAA_MODE=false
AUDIT_LEVEL=basic # (options: none, basic, full)
EOF
fi

if [ -f .env.template ] && [ ! -f .env ]; then
    cp .env.template .env
    log "Created .env file from .env.template. Please update it with your credentials."
fi

cat <<MSG

Setup complete!

- Python virtual environment is ready and can be activated with:
  source .venv/bin/activate

- Python dependencies are installed. Start the backend with:
  uvicorn api:app --reload

- Node.js dependencies are installed. Start the frontend with:
  npm start

- A .env file has been created. Make sure to fill in your API keys and other secrets.

Enjoy building your Telemedicine Platform!
MSG