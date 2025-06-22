# File: src/backend/main.py
# This sets up the main API application using FastAPI.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Healthcare Coordination API - Development")

# --- Middleware Configuration ---
# CORS (Cross-Origin Resource Sharing) middleware allows your React frontend
# (running on localhost:3000) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of your frontend app
    allow_credentials=True,                   # Allows cookies to be included in requests
    allow_methods=["*"],                      # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                      # Allows all request headers
)

# --- API Endpoints ---

@app.get("/health")
async def health_check():
    """
    A simple endpoint to verify that the API is running and healthy.
    Useful for monitoring and uptime checks.
    """
    return {"status": "healthy", "environment": "development"}

@app.post("/api/users")
async def create_user(user_data: dict):
    """
    A basic endpoint for creating a new user.
    NOTE: This is a placeholder. In a production environment, you would
    add data validation, password hashing, and error handling here.
    """
    # TODO: Implement robust input validation (e.g., using Pydantic models).
    # TODO: Hash the password before storing it.
    # TODO: Add user to the database.
    print(f"Creating user with data: {user_data}")
    return {"message": "User creation endpoint called (placeholder)", "data": user_data}
