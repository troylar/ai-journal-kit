"""Package resource and template management."""

import shutil
from importlib.resources import files
from pathlib import Path


def get_template(name: str) -> Path:
    """Get path to a specific template resource.

    Args:
        name: Template filename (e.g., 'daily-template.md')

    Returns:
        Path to template file
    """
    template_files = files("ai_journal_kit.templates")
    return Path(str(template_files.joinpath(name)))


def copy_template(template_name: str, destination: Path):
    """Copy a single template file to destination.

    Args:
        template_name: Template filename
        destination: Destination path
    """
    source = get_template(template_name)
    shutil.copy2(source, destination)


def copy_ide_configs(ide: str, destination: Path):
    """Copy IDE-specific configs to journal location.

    Args:
        ide: IDE name (cursor, windsurf, claude-code, copilot, all)
        destination: Journal root directory
    """
    ide_configs_base = files("ai_journal_kit.templates").joinpath("ide-configs")

    ides_to_copy = ["cursor", "windsurf", "claude-code", "copilot"] if ide == "all" else [ide]

    for ide_name in ides_to_copy:
        ide_source = Path(str(ide_configs_base.joinpath(ide_name)))

        if not ide_source.exists():
            continue  # Skip if IDE config doesn't exist yet

        # For cursor, the source has .cursor/rules/*.mdc, copy to destination/.cursor/rules/
        if ide_name == "cursor":
            source_rules = ide_source / ".cursor" / "rules"
            if source_rules.exists():
                dest_dir = destination / ".cursor" / "rules"
                dest_dir.mkdir(parents=True, exist_ok=True)
                for mdc_file in source_rules.glob("*.mdc"):
                    shutil.copy2(mdc_file, dest_dir / mdc_file.name)

        elif ide_name == "windsurf":
            source_rules = ide_source / ".windsurf" / "rules"
            if source_rules.exists():
                dest_dir = destination / ".windsurf" / "rules"
                dest_dir.mkdir(parents=True, exist_ok=True)
                for md_file in source_rules.glob("*.md"):
                    shutil.copy2(md_file, dest_dir / md_file.name)

        elif ide_name == "claude-code":
            # CLAUDE.md goes in root and subdirectories
            for claude_file in ide_source.glob("**/CLAUDE.md"):
                rel_path = claude_file.relative_to(ide_source)
                dest_file = destination / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(claude_file, dest_file)

        elif ide_name == "copilot":
            github_dir = ide_source / ".github"
            if github_dir.exists():
                dest_github = destination / ".github"
                shutil.copytree(github_dir, dest_github, dirs_exist_ok=True)


def list_available_templates() -> list[str]:
    """List all available template files.

    Returns:
        List of template filenames
    """
    template_dir = files("ai_journal_kit.templates")
    return [f.name for f in Path(str(template_dir)).iterdir() if f.is_file()]
