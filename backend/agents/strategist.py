import os
from crewai import Agent, LLM
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

my_llm = LLM(
    model="groq/llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


strategist = Agent(
    role="Strategy Analyst",
    goal="Identify market gaps, opportunities, and pricing recommendations from competitor data. Be concise",
    backstory="Strategy expert who gives clear, actionable insights",
    tools=[],
    verbose=True,
    llm=my_llm,
    allow_delegation=False
)