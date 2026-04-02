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


critic = Agent(
    role="Quality Editor",
    goal="Review content for accuracy and give a quality score (1-10). Three sentence only.",
    backstory="Former managing editor at Forbes with 15 years experience",
    tools=[],
    verbose=True,
    llm=my_llm,
    allow_delegation=False
)