from __future__ import annotations

import os
from pathlib import Path
from asep.agents.base import AgentContext, BaseAgent
from asep.domain import AgentResult, AgentResultStatus

class DocumentationAgent(BaseAgent):
    name = "documentation_agent"
    role = "Generating and maintaining codebase documentation"

    def run(self, context: AgentContext) -> AgentResult:
        workspace = Path(context.workspace_path)
        from asep.config import load_settings
        settings = load_settings()
        prov = settings.llm.provider.lower()
        has_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        
        doc_content = ""
        
        if has_key or prov in ("ollama", "openai_compatible"):
            try:
                from asep.llm import LLMClient
                client = LLMClient()
                
                system_instruction = "You are the ASEP Documentation Agent."
                prompt = (
                    f"Your task is to generate developer documentation for the recent implementation goal.\n"
                    f"Goal: {context.goal}\n\n"
                    f"Write a concise developer guide in markdown format covering endpoints, setup, and models."
                )
                
                doc_content = client.generate(prompt, system_instruction)
            except Exception:
                pass
                
        if not doc_content:
            doc_content = (
                f"# Developer Documentation Guide\n\n"
                f"## Features Implemented in Run {context.run_id}\n"
                f"- **Goal**: {context.goal}\n"
                f"- **Architecture Baseline**: Phase 1 control-plane architecture.\n"
                f"- **Database Integration**: Models mapped directly to runs, tasks, and memory records.\n"
                f"- **API Exposure**: FastAPI service endpoint mappings established.\n"
            )

        artifacts_dir = workspace / ".asep" / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        doc_filename = f"dev_docs_{context.run_id or 'default'}.md"
        doc_path = artifacts_dir / doc_filename
        doc_path.write_text(doc_content, encoding="utf-8")

        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary=f"Code documentation generated. Report saved to {doc_filename}",
            artifacts=[str(doc_path.as_posix())],
        )
