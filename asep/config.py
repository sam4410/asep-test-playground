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


class ArtifactConfig(BaseModel):
    path: Path = Path(".asep/artifacts")


class FileConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    artifacts: ArtifactConfig = Field(default_factory=ArtifactConfig)


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

    return file_config
