from __future__ import annotations

import os
from pathlib import Path
from asep.agents.base import AgentContext, BaseAgent
from asep.domain import AgentResult, AgentResultStatus
from asep.tools.workspace import list_files, read_file

class CodingAgent(BaseAgent):
    name = "coding_agent"
    role = "Proposing code changes via patches"

    def run(self, context: AgentContext) -> AgentResult:
        # Kept for backwards compatibility
        agent = BackendCodingAgent()
        return agent.run(context)

class BackendCodingAgent(BaseAgent):
    name = "backend_coding_agent"
    role = "Backend API and service logic"

    def run(self, context: AgentContext) -> AgentResult:
        goal = context.goal
        workspace = Path(context.workspace_path)
        
        from asep.config import load_settings
        settings = load_settings()
        prov = settings.llm.provider.lower()
        has_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

        patch_content = ""
        target_file = ""

        if has_key or prov in ("ollama", "openai_compatible"):
            patch_content, target_file = _run_llm_coder(self.name, self.role, goal, workspace)

        if not patch_content or not target_file:
            # Fallback to mock backend API change
            target_file = "asep/api/main.py"
            patch_content = (
                "--- a/asep/api/main.py\n"
                "+++ b/asep/api/main.py\n"
                "@@ -15,4 +15,9 @@\n"
                " @app.get(\"/health\")\n"
                " def health() -> dict[str, str]:\n"
                "     return {\"status\": \"ok\"}\n"
                " \n"
                " \n"
                "+@app.get(\"/api/v1/projects\")\n"
                "+def list_projects() -> list[dict]:\n"
                "+    # Mock projects endpoint\n"
                "+    return [{\"id\": 1, \"name\": \"ASEP Platform\", \"status\": \"running\"}]\n"
                "+\n"
                "+\n"
                " @app.post(\"/plans\")\n"
            )

        patch_path = _save_patch(workspace, context.run_id, patch_content)

        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Backend patch for {target_file} saved to {patch_path.name}",
            artifacts=[str(patch_path.as_posix())],
        )

class FrontendCodingAgent(BaseAgent):
    name = "frontend_coding_agent"
    role = "Frontend user interface components"

    def run(self, context: AgentContext) -> AgentResult:
        goal = context.goal
        workspace = Path(context.workspace_path)
        
        from asep.config import load_settings
        settings = load_settings()
        prov = settings.llm.provider.lower()
        has_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

        patch_content = ""
        target_file = ""

        if has_key or prov in ("ollama", "openai_compatible"):
            patch_content, target_file = _run_llm_coder(self.name, self.role, goal, workspace)

        if not patch_content or not target_file:
            # Fallback to mock frontend UI dashboard component
            target_file = "static/dashboard.js"
            patch_content = (
                "--- /dev/null\n"
                "+++ b/static/dashboard.js\n"
                "@@ -0,0 +1,10 @@\n"
                "+// ASEP Frontend Dashboard Component\n"
                "+function renderDashboard() {\n"
                "+    console.log(\"Initializing ASEP Dashboard UI...\");\n"
                "+    const container = document.getElementById(\"app\");\n"
                "+    if (container) {\n"
                "+        container.innerHTML = `\n"
                "+            <div class=\"card\">\n"
                "+                <h1>ASEP Control Panel</h1>\n"
                "+                <p>Welcome to your autonomous engineering platform dashboard.</p>\n"
                "+            </div>\n"
                "+        `;\n"
                "+    }\n"
                "+}\n"
            )

        patch_path = _save_patch(workspace, context.run_id, patch_content)

        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Frontend patch for {target_file} saved to {patch_path.name}",
            artifacts=[str(patch_path.as_posix())],
        )

class DatabaseCodingAgent(BaseAgent):
    name = "database_coding_agent"
    role = "Database models, schemas, and migrations"

    def run(self, context: AgentContext) -> AgentResult:
        goal = context.goal
        workspace = Path(context.workspace_path)
        
        from asep.config import load_settings
        settings = load_settings()
        prov = settings.llm.provider.lower()
        has_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

        patch_content = ""
        target_file = ""

        if has_key or prov in ("ollama", "openai_compatible"):
            patch_content, target_file = _run_llm_coder(self.name, self.role, goal, workspace)

        if not patch_content or not target_file:
            # Fallback to mock database model addition
            target_file = "asep/db/models.py"
            patch_content = (
                "--- a/asep/db/models.py\n"
                "+++ b/asep/db/models.py\n"
                "@@ -126,3 +126,14 @@\n"
                "     artifacts: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)\n"
                "     errors: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)\n"
                "     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)\n"
                "+\n"
                "+\n"
                "+class ProjectModel(Base):\n"
                "+    __tablename__ = \"projects\"\n"
                "+\n"
                "+    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))\n"
                "+    name: Mapped[str] = mapped_column(String(255), nullable=False)\n"
                "+    description: Mapped[str] = mapped_column(Text, nullable=True)\n"
                "+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)\n"
            )

        patch_path = _save_patch(workspace, context.run_id, patch_content)

        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Database patch for {target_file} saved to {patch_path.name}",
            artifacts=[str(patch_path.as_posix())],
        )

# Helper functions
def _run_llm_coder(agent_name: str, role: str, goal: str, workspace: Path) -> tuple[str, str]:
    try:
        from asep.llm import LLMClient
        client = LLMClient()
        files = list_files(workspace)
        
        file_context = ""
        for f in files[:5]:
            try:
                file_context += f"--- File: {f} ---\n{read_file(workspace, f)}\n\n"
            except Exception:
                continue

        system_instruction = f"You are the ASEP {agent_name}. Role: {role}."
        prompt = (
            f"Goal: \"{goal}\"\n\n"
            f"Existing Workspace Files:\n{files}\n\n"
            f"Relevant File Contents:\n{file_context}\n"
            f"Propose a code change in valid unified diff format. Specify the target file in the diff header.\n"
            f"Return ONLY the raw unified diff content, with no markdown code fences or conversational text."
        )
        
        content = client.generate(prompt, system_instruction)
        
        target_file = ""
        for line in content.splitlines():
            if line.startswith("+++ b/"):
                target_file = line[6:].strip()
                break
            elif line.startswith("+++ "):
                target_file = line[4:].strip()
                break
                
        return content, target_file
    except Exception:
        return "", ""


def _save_patch(workspace: Path, run_id: UUID | None, patch_content: str) -> Path:
    artifacts_dir = workspace / ".asep" / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    patch_filename = f"patch_{run_id or 'default'}.diff"
    patch_path = artifacts_dir / patch_filename
    patch_path.write_text(patch_content, encoding="utf-8")
    return patch_path
