import uuid
import httpx
from langchain_core.tools import tool

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import Message, Part, Role, SendMessageRequest


JOKE_AGENT_URL = "http://localhost:9000"


@tool
async def ask_joke_agent(request: str) -> str:
    """Delegate a joke request to the specialist Joke Agent.

    Use this when the user asks for a joke, wants to be entertained,
    or asks something humor-related.

    Args:
        request: A description of the joke request, e.g. 'tell me a programming joke'.

    Returns:
        The joke text from the specialist agent.
    """
    async with httpx.AsyncClient(timeout=30) as http:
        resolver = A2ACardResolver(httpx_client=http, base_url=JOKE_AGENT_URL)
        agent_card = await resolver.get_agent_card()

        config = ClientConfig(httpx_client=http, streaming=False)
        factory = ClientFactory(config)
        client = factory.create(agent_card)

        message = Message(
            role=Role.ROLE_USER,
            parts=[Part(text=request)],
            message_id=str(uuid.uuid4()),
        )
        send_request = SendMessageRequest(message=message)

        response_text = ""
        async for event in client.send_message(send_request):
            if event.HasField("message"):
                for part in event.message.parts:
                    if part.HasField("text"):
                        response_text += part.text
            elif event.HasField("task"):
                for msg in event.task.history:
                    if msg.role == Role.ROLE_AGENT:
                        for part in msg.parts:
                            if part.HasField("text"):
                                response_text += part.text

        return response_text or "(no response from joke agent)"
