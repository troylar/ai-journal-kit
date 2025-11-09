"""System manifest for tracking installed files and customizations.

The manifest tracks all system-installed files (templates, IDE configs) to detect
user customizations and prevent data loss during updates.
"""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal


@dataclass
class FileEntry:
    """Tracks a single system-installed file."""

    source: str  # e.g., "framework:gtd", "system:ide-config"
    installed_at: str  # ISO timestamp
    hash: str  # SHA256 hash of file content
    customized: bool = False  # Whether user has modified the file


@dataclass
class Manifest:
    """Tracks all system-installed files and their customization state."""

    version: str = "1.0.0"
    framework: str = "default"
    files: dict[str, FileEntry] = None

    def __post_init__(self):
        """Initialize files dict if not provided."""
        if self.files is None:
            self.files = {}

    @staticmethod
    def load(manifest_path: Path) -> "Manifest":
        """Load manifest from JSON file.

        Args:
            manifest_path: Path to .system-manifest.json

        Returns:
            Manifest instance
        """
        if not manifest_path.exists():
            return Manifest()

        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)

        # Convert file entries from dict to FileEntry objects
        files = {}
        for file_path, entry_data in data.get("files", {}).items():
            files[file_path] = FileEntry(**entry_data)

        return Manifest(
            version=data.get("version", "1.0.0"),
            framework=data.get("framework", "default"),
            files=files,
        )

    def save(self, manifest_path: Path):
        """Save manifest to JSON file.

        Args:
            manifest_path: Path to .system-manifest.json
        """
        # Convert FileEntry objects to dicts
        files_dict = {path: asdict(entry) for path, entry in self.files.items()}

        data = {"version": self.version, "framework": self.framework, "files": files_dict}

        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_file(
        self,
        file_path: Path,
        source: str,
        customized: bool = False,
        relative_to: Path | None = None,
    ):
        """Add or update a file in the manifest.

        Args:
            file_path: Absolute path to file
            source: Source identifier (e.g., "framework:gtd", "system:ide-config")
            customized: Whether file is customized
            relative_to: Make path relative to this directory (for portability)
        """
        # Use relative path for portability
        if relative_to:
            try:
                file_path = file_path.relative_to(relative_to)
            except ValueError:
                pass  # Keep absolute if not relative

        file_key = str(file_path)
        file_hash = self._compute_hash(
            file_path if file_path.is_absolute() else relative_to / file_path
        )

        self.files[file_key] = FileEntry(
            source=source,
            installed_at=datetime.now().isoformat(),
            hash=file_hash,
            customized=customized,
        )

    def is_customized(self, file_path: Path, relative_to: Path | None = None) -> bool:
        """Check if a file has been customized by the user.

        Args:
            file_path: Path to file (absolute or relative)
            relative_to: Make path relative to this directory

        Returns:
            True if file is customized, False otherwise
        """
        # Use relative path for lookup
        if relative_to and file_path.is_absolute():
            try:
                file_path = file_path.relative_to(relative_to)
            except ValueError:
                pass

        file_key = str(file_path)

        # Not tracked = not customized (new file or system hasn't seen it)
        if file_key not in self.files:
            return False

        entry = self.files[file_key]

        # Check if marked as customized
        if entry.customized:
            return True

        # Compare current hash with tracked hash
        actual_path = file_path if file_path.is_absolute() else relative_to / file_path
        if not actual_path.exists():
            return False

        current_hash = self._compute_hash(actual_path)
        return current_hash != entry.hash

    def mark_customized(self, file_path: Path, relative_to: Path | None = None):
        """Mark a file as customized.

        Args:
            file_path: Path to file
            relative_to: Make path relative to this directory
        """
        if relative_to and file_path.is_absolute():
            try:
                file_path = file_path.relative_to(relative_to)
            except ValueError:
                pass

        file_key = str(file_path)
        if file_key in self.files:
            self.files[file_key].customized = True

    def update_hash(self, file_path: Path, relative_to: Path | None = None):
        """Update the hash for a file after modification.

        Args:
            file_path: Path to file
            relative_to: Make path relative to this directory
        """
        if relative_to and file_path.is_absolute():
            try:
                file_path = file_path.relative_to(relative_to)
            except ValueError:
                pass

        file_key = str(file_path)
        actual_path = file_path if file_path.is_absolute() else relative_to / file_path

        if file_key in self.files and actual_path.exists():
            self.files[file_key].hash = self._compute_hash(actual_path)
            self.files[file_key].customized = False  # Reset customized flag

    def get_customized_files(self, source_filter: str | None = None) -> list[str]:
        """Get list of customized files.

        Args:
            source_filter: Only return files from this source (e.g., "framework:gtd")

        Returns:
            List of file paths that have been customized
        """
        customized = []
        for file_path, entry in self.files.items():
            if source_filter and not entry.source.startswith(source_filter):
                continue
            if entry.customized or self.is_customized(Path(file_path)):
                customized.append(file_path)
        return customized

    @staticmethod
    def _compute_hash(file_path: Path) -> str:
        """Compute SHA256 hash of file content.

        Args:
            file_path: Path to file

        Returns:
            Hex digest of file hash
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()


def is_in_safe_zone(file_path: Path, journal_path: Path) -> bool:
    """Check if file is in user-owned safe zone.

    Safe zones are never auto-modified by the system:
    - .ai-instructions/
    - .framework-backups/
    - daily/, projects/, people/, memories/, areas/, resources/, archive/

    Args:
        file_path: Path to check
        journal_path: Journal root directory

    Returns:
        True if file is in safe zone
    """
    try:
        relative = file_path.relative_to(journal_path)
    except ValueError:
        return False  # Not in journal

    safe_dirs = {
        ".ai-instructions",
        ".framework-backups",
        "daily",
        "projects",
        "people",
        "memories",
        "areas",
        "resources",
        "archive",
    }

    # Check if file is directly in or under a safe directory
    parts = relative.parts
    return len(parts) > 0 and parts[0] in safe_dirs


CustomizationAction = Literal["keep", "move", "replace", "diff", "cancel"]
