from crewai import Task
from backend.agents.strategist import strategist
from backend.tasks.research_task import research_task

strategy_task = Task(
    description="""
    Based on research, output in 3 lines max:
    1. One market gap (10 words)
    2. One opportunity (10 words)
    3. One pricing suggestion (10 words)
    
    Be EXTREMELY brief.
    """,
    expected_output="3 short lines: gap, opportunity, pricing",
    agent=strategist,
    context=[research_task],
    output_file="output/strategy.md"
)