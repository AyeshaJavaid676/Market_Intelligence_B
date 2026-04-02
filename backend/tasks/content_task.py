from crewai import Task
from backend.agents.writer import writer
from backend.tasks.research_task import research_task
from backend.tasks.strategy_task import strategy_task

content_task = Task(
    description="""
    Create brief content:
    - 2 blog titles (no outlines)
    - 3 social posts (10 words each)
    - 1 email subject line
    
    Keep extremely short.
    """,
    expected_output="Short markdown with titles, posts, subject",
    agent=writer,
    context=[research_task, strategy_task],
    output_file="output/content.md"
)