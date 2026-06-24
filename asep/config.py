from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectConfig(BaseModel):
    name: str = "ASEP"
    workspace_path: Path = Path(".")


class LLMConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-5"
    api_base: str | None = None


class DatabaseConfig(BaseModel):
    url: str = "postgresql+psycopg://asep:asep@localhost:5432/asep"


class ExecutionConfig(BaseModel):
    require_human_approval: bool = True
    max_task_retries: int = 1
    sandbox_type: str = "local"
    max_self_healing_attempts: int = 3
    validation_command: str = "pytest"


class ArtifactConfig(BaseModel):
    path: Path = Path(".asep/artifacts")


class GitConfig(BaseModel):
    enabled: bool = False
    github_token: str | None = None
    github_repo: str | None = None
    base_branch: str = "main"


class FileConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    artifacts: ArtifactConfig = Field(default_factory=ArtifactConfig)
    git: GitConfig = Field(default_factory=GitConfig)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    asep_env: str = Field(default="local", alias="ASEP_ENV")
    asep_log_level: str = Field(default="info", alias="ASEP_LOG_LEVEL")
    asep_artifacts_path: Path | None = Field(default=None, alias="ASEP_ARTIFACTS_PATH")
    asep_require_human_approval: bool | None = Field(
        default=None, alias="ASEP_REQUIRE_HUMAN_APPROVAL"
    )
    asep_max_task_retries: int | None = Field(default=None, alias="ASEP_MAX_TASK_RETRIES")
    asep_llm_provider: str | None = Field(default=None, alias="ASEP_LLM_PROVIDER")
    asep_llm_model: str | None = Field(default=None, alias="ASEP_LLM_MODEL")
    asep_llm_api_base: str | None = Field(default=None, alias="ASEP_LLM_API_BASE")
    asep_sandbox_type: str | None = Field(default=None, alias="ASEP_SANDBOX_TYPE")
    asep_max_self_healing_attempts: int | None = Field(default=None, alias="ASEP_MAX_SELF_HEALING_ATTEMPTS")
    asep_validation_command: str | None = Field(default=None, alias="ASEP_VALIDATION_COMMAND")
    asep_git_enabled: bool | None = Field(default=None, alias="ASEP_GIT_ENABLED")
    asep_github_token: str | None = Field(default=None, alias="ASEP_GITHUB_TOKEN")
    asep_github_repo: str | None = Field(default=None, alias="ASEP_GITHUB_REPO")
    asep_git_base_branch: str | None = Field(default=None, alias="ASEP_GIT_BASE_BRANCH")


def load_file_config(path: Path = Path("asep.yaml")) -> FileConfig:
    if not path.exists():
        return FileConfig()

    data: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return FileConfig.model_validate(data)


def load_settings(config_path: Path = Path("asep.yaml")) -> FileConfig:
    file_config = load_file_config(config_path)
    env_settings = Settings()

    if env_settings.database_url:
        file_config.database.url = env_settings.database_url

    if file_config.database.url.startswith("postgresql://"):
        file_config.database.url = file_config.database.url.replace("postgresql://", "postgresql+psycopg://", 1)
    if env_settings.asep_artifacts_path:
        file_config.artifacts.path = env_settings.asep_artifacts_path
    if env_settings.asep_require_human_approval is not None:
        file_config.execution.require_human_approval = env_settings.asep_require_human_approval
    if env_settings.asep_max_task_retries is not None:
        file_config.execution.max_task_retries = env_settings.asep_max_task_retries
    if env_settings.asep_llm_provider:
        file_config.llm.provider = env_settings.asep_llm_provider
    if env_settings.asep_llm_model:
        file_config.llm.model = env_settings.asep_llm_model
    if env_settings.asep_llm_api_base:
        file_config.llm.api_base = env_settings.asep_llm_api_base
    if env_settings.asep_sandbox_type:
        file_config.execution.sandbox_type = env_settings.asep_sandbox_type
    if env_settings.asep_max_self_healing_attempts is not None:
        file_config.execution.max_self_healing_attempts = env_settings.asep_max_self_healing_attempts
    if env_settings.asep_validation_command:
        file_config.execution.validation_command = env_settings.asep_validation_command
    if env_settings.asep_git_enabled is not None:
        file_config.git.enabled = env_settings.asep_git_enabled
    if env_settings.asep_github_token:
        file_config.git.github_token = env_settings.asep_github_token
    if env_settings.asep_github_repo:
        file_config.git.github_repo = env_settings.asep_github_repo
    if env_settings.asep_git_base_branch:
        file_config.git.base_branch = env_settings.asep_git_base_branch

    return file_config
