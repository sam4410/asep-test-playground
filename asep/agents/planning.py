from __future__ import annotations

import json
import logging
import os

from asep.agents.base import AgentContext, BaseAgent
from asep.domain import AgentResult, AgentResultStatus, RequirementSpec, Task
from asep.tasking import resolve_execution_order

logger = logging.getLogger("asep.agents.planning")



class ProductManagerAgent(BaseAgent):
    name = "product_manager"
    role = "Requirement understanding and acceptance criteria"

    def create_requirement_spec(self, goal: str) -> RequirementSpec:
        return RequirementSpec(
            goal=goal,
            features=[goal],
            constraints=["Human approval is required before code changes are applied."],
            assumptions=["Phase 1 uses PostgreSQL for shared memory and task queue state."],
            acceptance_criteria=[
                "A structured implementation plan is created.",
                "Tasks are persisted and reviewable.",
            ],
            open_questions=[],
        )

    def run(self, context: AgentContext) -> AgentResult:
        spec = self.create_requirement_spec(context.goal)
        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Created requirement spec for: {spec.goal}",
            artifacts=[],
        )


class ArchitectAgent(BaseAgent):
    name = "architect"
    role = "Repo inspection and architecture boundaries"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=(
                "Architecture baseline: Python 3.12, LangGraph orchestration, "
                "PostgreSQL persistence, human-approved patch application."
            ),
            artifacts=[],
        )


class PlannerAgent(BaseAgent):
    name = "planner"
    role = "Task graph creation"

    def create_initial_tasks(self, goal: str) -> list[Task]:
        # Try LLM-based planning first if credentials exist
        from asep.config import load_settings
        settings = load_settings()
        prov = settings.llm.provider.lower()
        has_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

        if has_key or prov in ("ollama", "openai_compatible"):
            try:
                from asep.llm import LLMClient
                client = LLMClient()
                system_instruction = (
                    "You are the ASEP Planner Agent. Your job is to break down a high-level requirement goal "
                    "into a structured task list. Available agents (owners) are: product_manager, architect, "
                    "database_coding_agent, backend_coding_agent, frontend_coding_agent, refactoring_agent, "
                    "documentation_agent, review_agent."
                )
                prompt = (
                    f"Requirement Goal: \"{goal}\"\n\n"
                    "Generate a JSON array of tasks where each task object has:\n"
                    "- title: short title string\n"
                    "- description: short description string\n"
                    "- owner: one of the available agents\n"
                    "- priority: integer priority (lower runs first, e.g. 10, 20)\n"
                    "- dependencies: list of task titles this task depends on (or empty list)\n\n"
                    "Return ONLY the raw JSON array. Do not include markdown code blocks or wrapping."
                )
                response_text = client.generate(prompt, system_instruction)
                if "```" in response_text:
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                response_text = response_text.strip()
                
                tasks_data = json.loads(response_text)
                
                tasks = []
                title_to_task = {}
                for t_data in tasks_data:
                    task = Task(
                        title=t_data["title"],
                        description=t_data["description"],
                        owner=t_data["owner"],
                        priority=t_data.get("priority", 50)
                    )
                    tasks.append(task)
                    title_to_task[t_data["title"]] = task
                    
                for t_data in tasks_data:
                    task = title_to_task.get(t_data["title"])
                    if task:
                        for dep_title in t_data.get("dependencies", []):
                            dep_task = title_to_task.get(dep_title)
                            if dep_task:
                                task.dependencies.append(dep_task.id)
                                
                resolve_execution_order(tasks)
                return tasks
            except Exception as e:
                logger.warning(f"LLM planning failed, falling back to rule-based planning: {e}")

        # Fallback to rule-based planning
        # Always start with requirement and architecture tasks

        requirement_task = Task(
            title="Confirm requirement spec",
            description=f"Convert the goal into structured acceptance criteria: {goal}",
            owner="product_manager",
            priority=10,
        )
        architecture_task = Task(
            title="Inspect architecture",
            description="Detect project conventions and implementation boundaries.",
            owner="architect",
            dependencies=[requirement_task.id],
            priority=20,
        )
        
        coding_tasks = []
        gl = goal.lower()
        
        # Check Database
        db_task = None
        if any(w in gl for w in ["db", "database", "table", "schema", "migration", "sql"]):
            db_task = Task(
                title="Design database schema and models",
                description=f"Define the PostgreSQL tables and SQLAlchemy models required for: {goal}",
                owner="database_coding_agent",
                dependencies=[architecture_task.id],
                priority=30,
            )
            coding_tasks.append(db_task)
            
        # Check Backend
        backend_task = None
        if any(w in gl for w in ["backend", "api", "endpoint", "service", "route", "controller", "logger"]):
            backend_deps = [db_task.id] if db_task else [architecture_task.id]
            backend_task = Task(
                title="Implement backend endpoints and business logic",
                description=f"Create REST API routes and business logic in FastAPI/Uvicorn for: {goal}",
                owner="backend_coding_agent",
                dependencies=backend_deps,
                priority=40,
            )
            coding_tasks.append(backend_task)
            
        # Check Frontend
        if any(w in gl for w in ["frontend", "ui", "screen", "component", "dashboard", "css", "html", "react"]):
            frontend_deps = []
            if coding_tasks:
                frontend_deps = [coding_tasks[-1].id]
            else:
                frontend_deps = [architecture_task.id]
                
            frontend_task = Task(
                title="Develop frontend dashboard components",
                description=f"Build modern UI views, layout styling, and client state handling for: {goal}",
                owner="frontend_coding_agent",
                dependencies=frontend_deps,
                priority=50,
            )
            coding_tasks.append(frontend_task)
            
        # Default fallback coding task if no keywords match
        if not coding_tasks:
            default_coding = Task(
                title="Implement core logic patch",
                description=f"Develop code changes to address the request: {goal}",
                owner="backend_coding_agent",
                dependencies=[architecture_task.id],
                priority=30,
            )
            coding_tasks.append(default_coding)
            
        # Refactoring task depends on last coding task
        refactor_task = Task(
            title="Refactor and format code",
            description="Verify code quality, cleanup layout, and verify style compliance.",
            owner="refactoring_agent",
            dependencies=[coding_tasks[-1].id],
            priority=60,
        )
        
        # Documentation task depends on refactoring task
        doc_task = Task(
            title="Update developer docs",
            description="Generate developer guides and documentation for new features.",
            owner="documentation_agent",
            dependencies=[refactor_task.id],
            priority=70,
        )
        
        # Review task depends on documentation task
        review_task = Task(
            title="Review proposed changes",
            description="Perform final threat model, code review risk assessment, and merge approval.",
            owner="review_agent",
            dependencies=[doc_task.id],
            priority=80,
        )
        
        tasks = [requirement_task, architecture_task] + coding_tasks + [refactor_task, doc_task, review_task]
        resolve_execution_order(tasks)
        return tasks

    def run(self, context: AgentContext) -> AgentResult:
        tasks = self.create_initial_tasks(context.goal)
        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Created {len(tasks)} dynamic Phase 1 tasks.",
            artifacts=[],
        )
