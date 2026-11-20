from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant that can write and run Python code.',
    instruction=("Answer user questions to the best of your knowledge"
                 "write python code and explain"),
    code_executor=BuiltInCodeExecutor()
)
