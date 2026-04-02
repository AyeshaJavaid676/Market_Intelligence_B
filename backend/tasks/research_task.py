from crewai import Task
from backend.agents.researcher import researcher

research_task = Task(
    description="""
    Research {topic}. Find 2 competitors only.
    
    For each: name, price (one number), USP (5 words), review (5 words).
    
    Output as JSON only. NO explanations. Keep VERY short.
    """,
    expected_output="JSON with 2 competitors: name, price, usp, review",
    agent=researcher,
    output_file="output/research.json"
)