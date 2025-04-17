#!/usr/bin/env python
"""
Agent Flows API

A simple API for managing automated agent workflows and tasks.
"""

import logging
import os
from typing import Dict, List, Optional, Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agent Flows API",
    description="API for managing automated agent workflows and tasks",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production to be more restrictive
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class Agent(BaseModel):
    """Model representing an agent in the system."""
    
    id: Optional[str] = Field(None, description="Unique identifier for the agent")
    name: str = Field(..., description="Name of the agent")
    description: str = Field(..., description="Description of the agent's purpose")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    config: Dict = Field(default_factory=dict, description="Agent configuration parameters")


class Workflow(BaseModel):
    """Model representing a workflow of connected agents."""
    
    id: Optional[str] = Field(None, description="Unique identifier for the workflow")
    name: str = Field(..., description="Name of the workflow")
    description: str = Field(..., description="Description of the workflow")
    agents: List[str] = Field(..., description="List of agent IDs in this workflow")
    connections: List[Dict] = Field(default_factory=list, description="Connections between agents")


class ExecutionResult(BaseModel):
    """Model representing the result of a workflow execution."""
    
    workflow_id: str = Field(..., description="ID of the executed workflow")
    status: str = Field(..., description="Status of the execution")
    result: Dict = Field(default_factory=dict, description="Execution results")
    logs: List[str] = Field(default_factory=list, description="Execution logs")


# In-memory data stores (replace with a database in production)
agents_db = {}
workflows_db = {}


# API Routes
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Agent Flows API",
        "version": "0.1.0",
        "status": "running",
    }


@app.post("/agents/", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(agent: Agent):
    """Create a new agent."""
    # Generate a simple ID if none provided
    if not agent.id:
        agent.id = f"agent_{len(agents_db) + 1}"
    
    if agent.id in agents_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Agent with ID {agent.id} already exists"
        )
    
    agents_db[agent.id] = agent.dict()
    logger.info(f"Created agent: {agent.id}")
    return agent


@app.get("/agents/", response_model=List[Agent])
async def list_agents():
    """List all agents."""
    return list(agents_db.values())


@app.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    if agent_id not in agents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Agent with ID {agent_id} not found"
        )
    
    return agents_db[agent_id]


@app.post("/workflows/", response_model=Workflow, status_code=status.HTTP_201_CREATED)
async def create_workflow(workflow: Workflow):
    """Create a new workflow."""
    # Generate a simple ID if none provided
    if not workflow.id:
        workflow.id = f"workflow_{len(workflows_db) + 1}"
    
    if workflow.id in workflows_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Workflow with ID {workflow.id} already exists"
        )
    
    # Validate that all referenced agents exist
    for agent_id in workflow.agents:
        if agent_id not in agents_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Agent with ID {agent_id} does not exist"
            )
    
    workflows_db[workflow.id] = workflow.dict()
    logger.info(f"Created workflow: {workflow.id}")
    return workflow


@app.get("/workflows/", response_model=List[Workflow])
async def list_workflows():
    """List all workflows."""
    return list(workflows_db.values())


@app.get("/workflows/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID."""
    if workflow_id not in workflows_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Workflow with ID {workflow_id} not found"
        )
    
    return workflows_db[workflow_id]


@app.post("/workflows/{workflow_id}/execute", response_model=ExecutionResult)
async def execute_workflow(workflow_id: str):
    """Execute a workflow and return the results."""
    if workflow_id not in workflows_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Workflow with ID {workflow_id} not found"
        )
    
    # In a real implementation, this would actually execute the workflow
    # For this demo, we just return a mock result
    logger.info(f"Executing workflow: {workflow_id}")
    
    return ExecutionResult(
        workflow_id=workflow_id,
        status="completed",
        result={"message": "Workflow executed successfully"},
        logs=["Started workflow execution", "Workflow completed"]
    )


if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the application with uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
