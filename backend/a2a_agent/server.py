import uvicorn
from starlette.applications import Starlette
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_jsonrpc_routes, create_agent_card_routes
from a2a.types import AgentCard, AgentSkill, AgentCapabilities, AgentInterface
from a2a.utils.constants import TransportProtocol

from joke_agent_executor import JokeAgentExecutor


def build_agent_card() -> AgentCard:
    skill = AgentSkill(
        id="tell_joke",
        name="Tell a Joke",
        description="Returns a short programming joke",
        tags=["humor", "jokes", "programming"],
        examples=["tell me a joke", "make me laugh", "I need a programming joke"],
    )
    return AgentCard(
        name="Joke Agent",
        description="A specialist agent that tells programming jokes",
        version="0.1.0",
        capabilities=AgentCapabilities(streaming=False),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[skill],
        supported_interfaces=[
            AgentInterface(url="http://localhost:9000/", protocol_binding=TransportProtocol.JSONRPC)
        ],
    )


def main():
    agent_card = build_agent_card()
    handler = DefaultRequestHandler(
        agent_executor=JokeAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )
    routes = create_agent_card_routes(agent_card) + create_jsonrpc_routes(handler, rpc_url="/")
    app = Starlette(routes=routes)
    uvicorn.run(app, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
