"""Package resource and template management."""

import shutil
from importlib.resources import files
from pathlib import Path


def resolve_template(template_name: str, journal_path: Path) -> Path | None:
    """Resolve template path using priority order.

    Priority:
    1. .ai-instructions/templates/ (user overrides - highest priority)
    2. Journal root (current framework templates)
    3. Package default (fallback)

    Args:
        template_name: Template filename (e.g., 'daily-template.md')
        journal_path: Journal root directory

    Returns:
        Path to template file, or None if not found
    """
    # Highest priority: user overrides in .ai-instructions/templates/
    user_template = journal_path / ".ai-instructions" / "templates" / template_name
    if user_template.exists():
        return user_template

    # Medium priority: journal root (current framework templates)
    journal_template = journal_path / template_name
    if journal_template.exists():
        return journal_template

    # Lowest priority: package default
    try:
        return get_template(template_name)
    except (FileNotFoundError, ValueError):
        return None


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


def copy_ide_configs(ide: str, destination: Path, framework: str = "default"):
    """Copy IDE-specific configs to journal location.

    Args:
        ide: IDE name (cursor, windsurf, claude-code, copilot, all)
        destination: Journal root directory
        framework: Framework name to replace {framework} placeholders (default: "default")
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
                    # Read, replace placeholders, write
                    content = mdc_file.read_text(encoding="utf-8")
                    content = content.replace("{framework}", framework)
                    (dest_dir / mdc_file.name).write_text(content, encoding="utf-8")

        elif ide_name == "windsurf":
            source_rules = ide_source / ".windsurf" / "rules"
            if source_rules.exists():
                dest_dir = destination / ".windsurf" / "rules"
                dest_dir.mkdir(parents=True, exist_ok=True)
                for md_file in source_rules.glob("*.md"):
                    # Read, replace placeholders, write
                    content = md_file.read_text(encoding="utf-8")
                    content = content.replace("{framework}", framework)
                    (dest_dir / md_file.name).write_text(content, encoding="utf-8")

        elif ide_name == "claude-code":
            # Copy all .md files from claude-code template to journal root
            for md_file in ide_source.glob("*.md"):
                dest_file = destination / md_file.name
                # Read, replace placeholders, write
                content = md_file.read_text(encoding="utf-8")
                content = content.replace("{framework}", framework)
                dest_file.write_text(content, encoding="utf-8")

        elif ide_name == "copilot":
            github_dir = ide_source / ".github"
            if github_dir.exists():
                dest_github = destination / ".github"
                dest_github.mkdir(parents=True, exist_ok=True)

                # Clean up old structure (copilot-instructions.md in .github root)
                old_copilot_file = dest_github / "copilot-instructions.md"
                if old_copilot_file.exists():
                    old_copilot_file.unlink()

                # Copy all files from .github, replacing {framework} placeholders
                for item in github_dir.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(github_dir)
                        dest_file = dest_github / rel_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)

                        # Replace placeholders in markdown files
                        if item.suffix in [".md", ".instructions.md"]:
                            content = item.read_text(encoding="utf-8")
                            content = content.replace("{framework}", framework)
                            dest_file.write_text(content, encoding="utf-8")
                        else:
                            shutil.copy2(item, dest_file)


def list_available_templates() -> list[str]:
    """List all available template files.

    Returns:
        List of template filenames
    """
    template_dir = files("ai_journal_kit.templates")
    return [f.name for f in Path(str(template_dir)).iterdir() if f.is_file()]
