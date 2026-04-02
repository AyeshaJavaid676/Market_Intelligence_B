import os
import time
from crewai import Agent
from crewai import LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

load_dotenv()

# Add a global delay function
def delayed_llm_call(*args, **kwargs):
    time.sleep(5)  # Wait 5 seconds before each LLM call
    return original_llm_call(*args, **kwargs)

my_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

tavily_tool = TavilySearchTool(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=2  # Reduced from 3 to 2
)

researcher = Agent(
    role="Market Researcher",
    goal="Find 2 competitors for {topic}. Be VERY brief. One line per item.",
    backstory="Expert researcher who gives concise, actionable data only.",
    tools=[tavily_tool],
    verbose=False,
    llm=my_llm,
    allow_delegation=False
)