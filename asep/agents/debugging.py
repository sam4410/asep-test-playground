from __future__ import annotations

import logging
from pathlib import Path
from asep.agents.base import AgentContext, BaseAgent
from asep.domain import AgentResult, AgentResultStatus
from asep.tools.sandbox import Sandbox
from asep.tools.workspace import read_file

logger = logging.getLogger("asep.agents.debugging")

class SelfHealingAgent(BaseAgent):
    name = "self_healing_agent"
    role = "Analyzing logs and self-healing test/lint failures"

    def run(self, context: AgentContext) -> AgentResult:
        # Implementing run for BaseAgent compliance
        return AgentResult(
            agent_name=self.name,
            status=AgentResultStatus.success,
            summary="Self healing agent active.",
            artifacts=[]
        )

    def heal_task(
        self,
        context: AgentContext,
        original_patch: str,
        test_cmd: str = "pytest",
        max_attempts: int = 3
    ) -> tuple[bool, str, str]:
        """
        Runs the self-healing validation and correction loop.
        Returns:
            (success: bool, final_patch: str, markdown_report: str)
        """
        sandbox = Sandbox(context.workspace_path)
        target_file = sandbox.extract_target_file(original_patch)
        
        # Check initial validation
        logger.info(f"Running initial validation in sandbox using command: {test_cmd}")
        success, output = sandbox.run_validation(original_patch, test_cmd)
        
        if success:
            logger.info("Original patch passed validation on first try.")
            report = (
                f"# Self-Healing Report\n\n"
                f"- **Goal**: {context.goal}\n"
                f"- **Target File**: {target_file}\n"
                f"- **Status**: SUCCESS\n\n"
                f"Original patch passed validation on the first attempt. No self-correction was necessary."
            )
            return True, original_patch, report

        logger.warning(f"Initial validation failed. Output length: {len(output)}. Starting self-healing...")
        
        history_entries = []
        current_patch = original_patch
        current_output = output
        
        history_entries.append(
            f"### Initial Validation\n"
            f"- **Status**: FAILED\n"
            f"- **Traceback / Output**:\n```\n{current_output}\n```\n"
        )
        
        attempt = 1
        healed_successfully = False
        
        from asep.config import load_settings
        settings = load_settings()
        
        while attempt <= max_attempts:
            logger.info(f"Self-healing attempt {attempt}/{max_attempts} for task on {target_file}")
            
            # Read current target file content
            current_file_content = ""
            try:
                if target_file:
                    current_file_content = read_file(context.workspace_path, target_file)
            except Exception as e:
                logger.warning(f"Failed to read current file content for {target_file}: {e}")

            # Call LLM Coder to fix the errors
            try:
                from asep.llm import LLMClient
                client = LLMClient()
                
                system_instruction = "You are the ASEP Self-Healing Debugging Agent."
                prompt = (
                    f"The patch you proposed for \"{target_file}\" failed verification.\n\n"
                    f"Goal: {context.goal}\n"
                    f"Target File: {target_file}\n\n"
                    f"--- Original Proposed Patch ---\n{original_patch}\n\n"
                    f"--- Current File Content (Unpatched) ---\n{current_file_content}\n\n"
                    f"--- Test/Validation Output ---\n{current_output}\n\n"
                    f"Instructions:\n"
                    f"1. Analyze the test/validation failure output carefully.\n"
                    f"2. Identify the root cause (e.g. syntax error, failed assertion, import error).\n"
                    f"3. Generate a corrected unified diff patch for \"{target_file}\" that fixes the issues.\n"
                    f"Return ONLY the corrected raw unified diff content, with no markdown code fences or conversational text."
                )
                
                response = client.generate(prompt, system_instruction)
                
                # Parse code fences cleanly
                new_patch = response.strip()
                if "```" in new_patch:
                    parts = new_patch.split("```")
                    for p in parts:
                        p_strip = p.strip()
                        if p_strip.startswith("diff\n") or p_strip.startswith("---") or p_strip.startswith("+++"):
                            new_patch = p_strip
                            break
                    if new_patch.startswith("diff"):
                        lines = new_patch.splitlines()
                        if lines and (lines[0].strip() == "diff" or lines[0].strip().startswith("diff ")):
                            new_patch = "\n".join(lines[1:])
                
                # Re-validate
                logger.info(f"Re-validating corrected patch for attempt {attempt}")
                val_success, val_output = sandbox.run_validation(new_patch, test_cmd)
                
                history_entries.append(
                    f"### Self-Healing Attempt {attempt}\n"
                    f"- **Status**: {'PASSED' if val_success else 'FAILED'}\n"
                    f"- **Proposed Fix Diff**:\n```diff\n{new_patch}\n```\n"
                    f"- **Traceback / Output**:\n```\n{val_output}\n```\n"
                )
                
                current_patch = new_patch
                current_output = val_output
                
                if val_success:
                    logger.info(f"Self-healing succeeded on attempt {attempt}!")
                    healed_successfully = True
                    break
                    
            except Exception as e:
                logger.error(f"Error during self-healing attempt {attempt}: {e}", exc_info=True)
                history_entries.append(
                    f"### Self-Healing Attempt {attempt}\n"
                    f"- **Status**: ERROR\n"
                    f"- **Details**: LLM generation failed: {e}\n"
                )
            
            attempt += 1

        # Build final report
        status_str = "SUCCESS" if healed_successfully else "FAILED"
        report = (
            f"# Self-Healing Debugging Report\n\n"
            f"- **Goal**: {context.goal}\n"
            f"- **Target File**: {target_file}\n"
            f"- **Total Attempts**: {min(attempt, max_attempts)} / {max_attempts}\n"
            f"- **Final Self-Correction Status**: **{status_str}**\n\n"
            f"--- \n\n"
            f"## Attempt History\n\n" + "\n".join(history_entries)
        )
        
        return healed_successfully, current_patch, report
