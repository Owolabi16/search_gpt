#!/usr/bin/env python
"""
Agent Flows API - Simplified Version
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Agent Flows API",
    description="Simplified API for testing",
    version="0.1.0",
)

class Message(BaseModel):
    """Simple message model"""
    content: str

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Agent Flows API",
        "version": "0.1.0",
        "status": "running",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/echo")
async def echo(message: Message):
    """Echo back the message."""
    return {"message": message.content}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the application with uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
