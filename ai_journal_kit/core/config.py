"""Configuration management for AI Journal Kit."""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from platformdirs import user_config_dir
from pydantic import BaseModel, Field, field_validator


class Config(BaseModel):
    """User's journal configuration."""

    journal_location: Path
    ide: Literal["cursor", "windsurf", "claude-code", "copilot", "all"]
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    use_symlink: bool = False
    symlink_source: Path | None = None

    @field_validator("journal_location", mode="before")
    @classmethod
    def expand_path(cls, v):
        """Expand ~ and resolve to absolute path."""
        if isinstance(v, str):
            return Path(v).expanduser().resolve()
        return Path(v).expanduser().resolve()

    class Config:
        json_encoders = {Path: str, datetime: lambda v: v.isoformat()}

    def model_dump_json(self, **kwargs) -> str:
        """Override to handle Path and datetime serialization."""
        data = self.model_dump(**kwargs)
        # Convert Path to str and datetime to isoformat
        if "journal_location" in data:
            data["journal_location"] = str(data["journal_location"])
        if "symlink_source" in data and data["symlink_source"]:
            data["symlink_source"] = str(data["symlink_source"])
        if "created_at" in data:
            data["created_at"] = data["created_at"].isoformat()
        if "last_updated" in data:
            data["last_updated"] = data["last_updated"].isoformat()
        return json.dumps(data, indent=2)


def get_config_path() -> Path:
    """Get platform-specific config file path."""
    config_dir = Path(user_config_dir("ai-journal-kit", appauthor=False))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config() -> Config | None:
    """Load config file if it exists."""
    config_path = get_config_path()
    if not config_path.exists():
        return None

    try:
        data = json.loads(config_path.read_text())
        # Parse datetime strings
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data and isinstance(data["last_updated"], str):
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return Config(**data)
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        from ai_journal_kit.utils.ui import error_console

        error_console.print(
            f"[yellow]Warning: Config file corrupted ({e}), using defaults[/yellow]"
        )
        return None


def save_config(config: Config):
    """Save config file."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(config.model_dump_json())


def update_config(**kwargs):
    """Update specific config fields."""
    config = load_config()
    if not config:
        raise ValueError("No configuration found. Run setup first.")

    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

    config.last_updated = datetime.now()
    save_config(config)
    return config
