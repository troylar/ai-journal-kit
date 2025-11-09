"""Configuration management for AI Journal Kit with multi-journal support."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

from platformdirs import user_config_dir
from pydantic import BaseModel, ConfigDict, Field, field_validator


class JournalProfile(BaseModel):
    """Configuration for a single journal."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    location: Path
    ide: Literal["cursor", "windsurf", "claude-code", "copilot", "all"]
    framework: Literal["default", "gtd", "para", "bullet-journal", "zettelkasten"] = "default"
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    use_symlink: bool = False
    symlink_source: Path | None = None

    @field_validator("location", mode="before")
    @classmethod
    def expand_path(cls, v):
        """Expand ~ and resolve to absolute path."""
        if isinstance(v, str):
            return Path(v).expanduser().resolve()
        return Path(v).expanduser().resolve()


class MultiJournalConfig(BaseModel):
    """Multi-journal configuration."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    active_journal: str = "default"
    journals: dict[str, JournalProfile] = Field(default_factory=dict)

    def get_active_profile(self) -> JournalProfile | None:
        """Get the currently active journal profile."""
        # Check environment variable override first
        env_journal = os.getenv("AI_JOURNAL")
        if env_journal and env_journal in self.journals:
            return self.journals[env_journal]

        # Use configured active journal
        return self.journals.get(self.active_journal)

    def has_journal(self, name: str) -> bool:
        """Check if a journal with given name exists."""
        return name in self.journals

    def add_journal(self, profile: JournalProfile):
        """Add a new journal profile."""
        self.journals[profile.name] = profile

    def remove_journal(self, name: str):
        """Remove a journal profile."""
        if name in self.journals:
            del self.journals[name]
            # If we deleted the active journal, switch to another one
            if self.active_journal == name and self.journals:
                self.active_journal = list(self.journals.keys())[0]

    def set_active(self, name: str):
        """Set the active journal."""
        if name not in self.journals:
            raise ValueError(f"Journal '{name}' not found")
        self.active_journal = name


# Backward compatibility: Old single-journal config
class Config(BaseModel):
    """Legacy single-journal configuration (for backward compatibility)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    journal_location: Path
    ide: Literal["cursor", "windsurf", "claude-code", "copilot", "all"]
    framework: Literal["default", "gtd", "para", "bullet-journal", "zettelkasten"] = "default"
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


def get_config_path() -> Path:
    """Get platform-specific config file path."""
    config_dir_str = os.getenv("AI_JOURNAL_CONFIG_DIR")
    if config_dir_str:
        config_dir = Path(config_dir_str)
    else:
        config_dir = Path(user_config_dir("ai-journal-kit", appauthor=False))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def migrate_legacy_config(legacy_data: dict) -> MultiJournalConfig:
    """Migrate old single-journal config to multi-journal format."""
    # Parse datetime strings
    if "created_at" in legacy_data and isinstance(legacy_data["created_at"], str):
        legacy_data["created_at"] = datetime.fromisoformat(legacy_data["created_at"])
    if "last_updated" in legacy_data and isinstance(legacy_data["last_updated"], str):
        legacy_data["last_updated"] = datetime.fromisoformat(legacy_data["last_updated"])

    # Create legacy config
    legacy_config = Config(**legacy_data)

    # Convert to multi-journal format
    profile = JournalProfile(
        name="default",
        location=legacy_config.journal_location,
        ide=legacy_config.ide,
        framework=legacy_config.framework,
        version=legacy_config.version,
        created_at=legacy_config.created_at,
        last_updated=legacy_config.last_updated,
        use_symlink=legacy_config.use_symlink,
        symlink_source=legacy_config.symlink_source,
    )

    multi_config = MultiJournalConfig(active_journal="default")
    multi_config.add_journal(profile)

    return multi_config


def load_config() -> Config | None:
    """Load config and return active journal as legacy Config object for backward compatibility.

    This function maintains backward compatibility by returning a Config object
    representing the active journal, even though internally we use MultiJournalConfig.
    """
    multi_config = load_multi_journal_config()
    if not multi_config:
        return None

    active_profile = multi_config.get_active_profile()
    if not active_profile:
        return None

    # Convert active profile back to legacy Config format
    return Config(
        journal_location=active_profile.location,
        ide=active_profile.ide,
        framework=active_profile.framework,
        version=active_profile.version,
        created_at=active_profile.created_at,
        last_updated=active_profile.last_updated,
        use_symlink=active_profile.use_symlink,
        symlink_source=active_profile.symlink_source,
    )


def load_multi_journal_config() -> MultiJournalConfig | None:
    """Load full multi-journal configuration."""
    config_path = get_config_path()
    if not config_path.exists():
        return None

    try:
        data = json.loads(config_path.read_text())

        # Detect if this is legacy format
        if "journal_location" in data and "journals" not in data:
            # Migrate legacy config
            multi_config = migrate_legacy_config(data)
            # Save migrated config
            save_multi_journal_config(multi_config)
            return multi_config

        # Parse as multi-journal config
        # Parse journal profiles
        journals = {}
        for name, profile_data in data.get("journals", {}).items():
            # Parse datetime strings
            if "created_at" in profile_data and isinstance(profile_data["created_at"], str):
                profile_data["created_at"] = datetime.fromisoformat(profile_data["created_at"])
            if "last_updated" in profile_data and isinstance(profile_data["last_updated"], str):
                profile_data["last_updated"] = datetime.fromisoformat(profile_data["last_updated"])

            # Ensure name is in profile_data (don't pass it twice)
            if "name" not in profile_data:
                profile_data["name"] = name

            journals[name] = JournalProfile(**profile_data)

        return MultiJournalConfig(
            active_journal=data.get("active_journal", "default"),
            journals=journals,
        )

    except (json.JSONDecodeError, ValueError, TypeError) as e:
        from ai_journal_kit.utils.ui import error_console

        error_console.print(
            f"[yellow]Warning: Config file corrupted ({e}), using defaults[/yellow]"
        )
        return None


def save_config(config: Config):
    """Save single journal config (legacy function for backward compatibility).

    Updates the active journal in the multi-journal config.
    """
    multi_config = load_multi_journal_config()
    if not multi_config:
        # No existing config - create new one with default journal
        profile = JournalProfile(
            name="default",
            location=config.journal_location,
            ide=config.ide,
            framework=config.framework,
            version=config.version,
            created_at=config.created_at,
            last_updated=config.last_updated,
            use_symlink=config.use_symlink,
            symlink_source=config.symlink_source,
        )
        multi_config = MultiJournalConfig(active_journal="default")
        multi_config.add_journal(profile)
    else:
        # Update active journal
        active_name = multi_config.active_journal
        profile = JournalProfile(
            name=active_name,
            location=config.journal_location,
            ide=config.ide,
            framework=config.framework,
            version=config.version,
            created_at=config.created_at,
            last_updated=datetime.now(),
            use_symlink=config.use_symlink,
            symlink_source=config.symlink_source,
        )
        multi_config.journals[active_name] = profile

    save_multi_journal_config(multi_config)


def save_multi_journal_config(config: MultiJournalConfig):
    """Save multi-journal configuration."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict for JSON serialization
    data = {
        "active_journal": config.active_journal,
        "journals": {},
    }

    for name, profile in config.journals.items():
        profile_data = {
            "name": profile.name,
            "location": str(profile.location),
            "ide": profile.ide,
            "framework": profile.framework,
            "version": profile.version,
            "created_at": profile.created_at.isoformat(),
            "last_updated": profile.last_updated.isoformat(),
            "use_symlink": profile.use_symlink,
        }
        if profile.symlink_source:
            profile_data["symlink_source"] = str(profile.symlink_source)
        data["journals"][name] = profile_data

    config_path.write_text(json.dumps(data, indent=2))


def update_config(**kwargs):
    """Update specific config fields in the active journal."""
    config = load_config()
    if not config:
        raise ValueError("No configuration found. Run setup first.")

    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

    config.last_updated = datetime.now()
    save_config(config)
    return config


def get_active_journal_name() -> str | None:
    """Get the name of the currently active journal."""
    # Check environment variable override first
    env_journal = os.getenv("AI_JOURNAL")
    if env_journal:
        return env_journal

    multi_config = load_multi_journal_config()
    if not multi_config:
        return None

    return multi_config.active_journal
