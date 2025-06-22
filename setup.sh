#!/usr/bin/env bash

set -e

# Determine package manager
if command -v apt-get > /dev/null; then
    PKG_MANAGER="apt-get"
    INSTALL_CMD="sudo apt-get install -y"
    UPDATE_CMD="sudo apt-get update"
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
elif command -v brew > /dev/null; then
    PKG_MANAGER="brew"
    INSTALL_CMD="brew install"
    UPDATE_CMD="brew update"
else
    echo "Unsupported OS or package manager not found."
    exit 1
fi

# Update repositories
$UPDATE_CMD

# Example packages required for this project
PACKAGES=(python3 python3-pip git)

for pkg in "${PACKAGES[@]}"; do
    $INSTALL_CMD "$pkg"
done

# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install Python dependencies if requirements file exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Node.js dependencies
if [ -f package.json ] && command -v npm >/dev/null; then
    npm install
fi

cat <<MSG
Setup complete using $PKG_MANAGER.
Activate the Python environment with 'source .venv/bin/activate'.
MSG
