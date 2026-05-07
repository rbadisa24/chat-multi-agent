from typing_extensions import override
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class JokeAgent:
    """Specialist joke agent powered by its own LangGraph ReAct loop.
    Note: no tools — pure LLM completion. Demonstrates that A2A agents
    can have their own internal complexity hidden from the caller.
    """
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPEN_API_KEY"))
        self._agent = create_react_agent(
            llm,
            tools=[],
            prompt="You are a specialist joke-telling agent. Reply with exactly ONE short, clean programming joke. No preamble.",
        )

    async def invoke(self, user_text: str) -> str:
        result = await self._agent.ainvoke(
            {"messages": [{"role": "user", "content": user_text or "Tell me a joke"}]}
        )
        return result["messages"][-1].content


class JokeAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = JokeAgent()

    @override
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_text = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                root = getattr(part, "root", part)
                if hasattr(root, "text"):
                    user_text += root.text

        result = await self.agent.invoke(user_text)
        await event_queue.enqueue_event(new_text_message(result))

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")