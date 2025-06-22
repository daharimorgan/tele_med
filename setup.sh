#!/usr/bin/env bash

set -e

# Detect operating system
OS_NAME="$(uname -s)"

# Helper to log messages
log() {
    echo "[setup] $1"
}

# Determine package manager
if command -v brew > /dev/null; then
    PKG_MANAGER="brew"
    INSTALL_CMD="brew install"
    UPDATE_CMD="brew update"
    PACKAGES=(python git)
elif command -v apt-get > /dev/null; then
    # The original Debian-based commands are commented out for environments using
    # Homebrew. Uncomment if you need apt-get support.
    # PKG_MANAGER="apt-get"
    # INSTALL_CMD="sudo apt-get install -y"
    # UPDATE_CMD="sudo apt-get update"
    echo "apt-get detected but brew is preferred. Skipping package installs."
    PKG_MANAGER="apt-get"
    INSTALL_CMD=":"
    UPDATE_CMD=":"
    PACKAGES=(python3 python3-pip git)
elif command -v yum > /dev/null; then
    PKG_MANAGER="yum"
    INSTALL_CMD="sudo yum install -y"
    UPDATE_CMD="sudo yum update -y"
elif command -v dnf > /dev/null; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
    UPDATE_CMD="sudo dnf update -y"
elif command -v pacman > /dev/null; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S --noconfirm"
    UPDATE_CMD="sudo pacman -Sy"
elif command -v choco > /dev/null; then
    PKG_MANAGER="choco"
    INSTALL_CMD="choco install -y"
    UPDATE_CMD="choco upgrade -y"
else
    echo "Unsupported OS or package manager not found."
    exit 1
fi

# Update repositories
log "Updating package lists using $PKG_MANAGER"
$UPDATE_CMD

# Example packages required for this project
if [ -z "${PACKAGES+x}" ]; then
    PACKAGES=(python3 python3-pip git)
fi

for pkg in "${PACKAGES[@]}"; do
    if ! command -v "${pkg%% *}" >/dev/null; then
        log "Installing $pkg"
        $INSTALL_CMD "$pkg"
    else
        log "$pkg already installed"
    fi
done

# Setup Python virtual environment
if [ ! -d .venv ]; then
    log "Creating Python virtual environment"
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip

# Install Python dependencies if requirements file exists
if [ -f requirements.txt ]; then
    log "Installing Python dependencies"
    pip install -r requirements.txt
fi

# Create environment file if template exists
if [ -f .env.template ] && [ ! -f .env ]; then
    cp .env.template .env
    log "Created .env from template"
fi

# Node.js dependencies
if [ -f package.json ] && command -v npm >/dev/null; then
    log "Installing Node dependencies"
    npm install
elif [ -f package.json ]; then
    log "package.json found but npm is missing. Please install Node.js"
fi

cat <<MSG
Setup complete using $PKG_MANAGER on $OS_NAME.
Activate the Python environment with 'source .venv/bin/activate'.
MSG
