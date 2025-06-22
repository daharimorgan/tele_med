# File: .env.development
#
# This file contains environment variables for the DEVELOPMENT environment.
# It should NOT be committed to version control.
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
