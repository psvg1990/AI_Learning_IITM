import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# W2 pipeline — the underlying engine
from src.pipeline.pipeline import ask_llm as _pipeline_ask_llm
from src.pipeline.pipeline import Question as _PipelineQuestion