import os
from crewai import Agent, LLM
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

my_llm = LLM(
    model="groq/llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5
)
writer = Agent(
    role="Content Creator",
    goal="Create 2 blog ideas, 3 social posts, 1 email. Short format.",
    backstory="Award-winning copywriter with expertise in B2B and DTC marketing who creates engaging, short-form content",
    tools=[],
    verbose=True,
    llm=my_llm,
    allow_delegation=False
)