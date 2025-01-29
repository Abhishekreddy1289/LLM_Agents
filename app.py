from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict
import uuid
import time
import numpy as np
from collections import defaultdict
import datetime
from config import model_name,api_key,api_version,azure_endpoint
from agent_llm import LLMAgent


app = FastAPI()
ai_agent = LLMAgent(
    api_key=api_key,
    openai_type="azure_openai",
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    model_name=model_name
)

class InteractionRequest(BaseModel):
    query: str

@app.post("/interaction/{id}")
async def track_interaction(id: str, request: InteractionRequest):
    try:
        response = ai_agent.llm(request.query, id)
        return {"answer":response}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")