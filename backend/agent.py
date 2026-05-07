import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from tools.sample_api import get_weather
from tools.a2a_client import ask_joke_agent

# Load environment variables
load_dotenv()

async def build_agent_async():
    # Create the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPEN_API_KEY"))

    mcp_path = os.path.abspath("mcp_server/server.py")
    
    mcp_client = MultiServerMCPClient(
        {
            "utility":{
                "command":"python",
                "args":[mcp_path],
                "transport":"stdio"
            }
        }
    )

    mcp_tools = await mcp_client.get_tools()
    tools = [get_weather, ask_joke_agent] + mcp_tools

    # Create the ReAct agent
    agent = create_react_agent(llm, tools=tools)

    return agent   
