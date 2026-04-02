import os
from crewai import Agent, LLM  # <--- Import LLM from crewai
from dotenv import load_dotenv

load_dotenv()

# Define using the CrewAI LLM wrapper (this satisfies Pydantic's string AND instance checks)
my_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

strategist = Agent(
    role="Strategy Analyst",
    goal="Develop execution plans",
    backstory="Expert in RAG workflows",
    llm=my_llm,  # Pydantic will now validate this as a proper 'instance'
    verbose=True,
    allow_delegation=False
)