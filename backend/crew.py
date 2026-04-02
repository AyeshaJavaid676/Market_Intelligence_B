import time
from crewai import Crew, Process
from backend.tasks.research_task import research_task
from backend.tasks.strategy_task import strategy_task
from backend.tasks.content_task import content_task
from backend.agents.researcher import researcher
from backend.agents.strategist import strategist
from backend.agents.writer import writer

def delay_callback(task):
    """Add delay between tasks to respect rate limits"""
    print(f"✅ Completed: {task.name}")
    time.sleep(15)  # ← 15 second delay

market_crew = Crew(
    agents=[researcher, strategist, writer],
    tasks=[research_task, strategy_task, content_task],
    process=Process.sequential,
    verbose=False,  # ← Reduce console output
    memory=False,  # ← Disable memory (removes OpenAI error)
    cache=True,
    task_callback=delay_callback  # ← Add delay between tasks
)