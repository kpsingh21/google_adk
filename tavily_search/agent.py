from google.adk.agents.llm_agent import Agent
# pip install -U langchain-tavily
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch

# 1. create the Langchain Tavily Tool
tavily_search = TavilySearch(
    max_results=5,
    topic='general',
)

# 2 Wrap it so ADK can use it
tavily_tool =LangchainTool(tool=tavily_search)

# 3. Give it to the agent like any other tool
root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[tavily_search]
)


