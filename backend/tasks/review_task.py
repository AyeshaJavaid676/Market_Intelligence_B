from crewai import Task
from backend.agents.critic import critic
from backend.tasks.research_task import research_task
from backend.tasks.strategy_task import strategy_task
from backend.tasks.content_task import content_task

review_task = Task(
    description="""
    Review all generated content for:
    
    1. Factual accuracy against source research (check if claims match)
    2. Grammar and readability
    3. Brand voice consistency
    4. Actionability (can client actually use this?)
    
    Provide:
    - Quality score (0-100)
    - Top 3 issues found (if any)
    - Top 3 strengths
    - Final verdict: APPROVE or NEEDS REVISION
    
    Be honest but constructive.
    """,
    expected_output="Review report with score, issues, strengths, verdict",
    agent=critic,
    context=[research_task, strategy_task, content_task],
    output_file="output/review.md"
)