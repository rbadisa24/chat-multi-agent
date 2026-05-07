from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from typing import Optional

from pydantic import BaseModel
# from agent import build_agent

from contextlib import asynccontextmanager
from fastapi import FastAPI

agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    from agent import build_agent_async
    agent = await build_agent_async()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    """Request model for chat messages."""
    message: str
    thread_id: Optional[str] = None
    

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat messages."""
    response = await agent.ainvoke({"messages": [{"role": "user", "content": request.message}]})
    final = response["messages"][-1].content
    # also surface intermediate steps for learning
    trace =[{"type": m.type,"content": str(m.content)[:200]} for m in response["messages"]]
    return {"response": final, "trace": trace}
