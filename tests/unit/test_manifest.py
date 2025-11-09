"""Unit tests for manifest module."""

import pytest

from ai_journal_kit.core.manifest import (
    FileEntry,
    Manifest,
    is_in_safe_zone,
)


@pytest.mark.unit
def test_file_entry_creation():
    """Test creating a FileEntry."""
    entry = FileEntry(
        source="framework:gtd",
        installed_at="2025-01-09T10:00:00",
        hash="abc123",
        customized=False,
    )

    assert entry.source == "framework:gtd"
    assert entry.installed_at == "2025-01-09T10:00:00"
    assert entry.hash == "abc123"
    assert entry.customized is False


@pytest.mark.unit
def test_manifest_creation():
    """Test creating a Manifest."""
    manifest = Manifest()

    assert manifest.version == "1.0.0"
    assert manifest.framework == "default"
    assert manifest.files == {}


@pytest.mark.unit
def test_manifest_post_init():
    """Test Manifest __post_init__ initializes files dict."""
    manifest = Manifest(version="2.0.0", framework="gtd", files=None)

    assert manifest.files == {}


@pytest.mark.unit
def test_manifest_save_and_load(tmp_path):
    """Test saving and loading a manifest."""
    manifest_path = tmp_path / ".system-manifest.json"

    # Create and save manifest
    manifest = Manifest(version="1.0.0", framework="gtd")
    manifest.files["daily-template.md"] = FileEntry(
        source="framework:gtd",
        installed_at="2025-01-09T10:00:00",
        hash="abc123",
        customized=False,
    )
    manifest.save(manifest_path)

    # Load and verify
    loaded = Manifest.load(manifest_path)

    assert loaded.version == "1.0.0"
    assert loaded.framework == "gtd"
    assert "daily-template.md" in loaded.files
    assert loaded.files["daily-template.md"].source == "framework:gtd"
    assert loaded.files["daily-template.md"].hash == "abc123"
    assert loaded.files["daily-template.md"].customized is False


@pytest.mark.unit
def test_manifest_load_missing_file(tmp_path):
    """Test loading manifest when file doesn't exist."""
    manifest_path = tmp_path / ".system-manifest.json"

    loaded = Manifest.load(manifest_path)

    assert loaded.version == "1.0.0"
    assert loaded.framework == "default"
    assert loaded.files == {}


@pytest.mark.unit
def test_manifest_save_creates_parent_directory(tmp_path):
    """Test that save creates parent directories if needed."""
    manifest_path = tmp_path / "nested" / "dirs" / ".system-manifest.json"

    manifest = Manifest()
    manifest.save(manifest_path)

    assert manifest_path.exists()
    assert manifest_path.parent.exists()


@pytest.mark.unit
def test_manifest_add_file_absolute_path(tmp_path):
    """Test adding a file with absolute path."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    manifest.add_file(test_file, source="framework:gtd")

    file_key = str(test_file)
    assert file_key in manifest.files
    assert manifest.files[file_key].source == "framework:gtd"
    assert manifest.files[file_key].hash != ""
    assert manifest.files[file_key].customized is False


@pytest.mark.unit
def test_manifest_add_file_relative_path(tmp_path):
    """Test adding a file with relative path."""
    manifest = Manifest()
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    test_file = journal_path / "test.md"
    test_file.write_text("test content")

    manifest.add_file(test_file, source="framework:gtd", relative_to=journal_path)

    # Should store as relative path
    assert "test.md" in manifest.files
    assert manifest.files["test.md"].source == "framework:gtd"


@pytest.mark.unit
def test_manifest_add_file_customized(tmp_path):
    """Test adding a file marked as customized."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    manifest.add_file(test_file, source="framework:gtd", customized=True)

    file_key = str(test_file)
    assert manifest.files[file_key].customized is True


@pytest.mark.unit
def test_manifest_is_customized_not_tracked(tmp_path):
    """Test is_customized for untracked file."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    assert manifest.is_customized(test_file) is False


@pytest.mark.unit
def test_manifest_is_customized_marked_as_customized(tmp_path):
    """Test is_customized when file is explicitly marked."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    manifest.add_file(test_file, source="framework:gtd", customized=True)

    assert manifest.is_customized(test_file) is True


@pytest.mark.unit
def test_manifest_is_customized_hash_changed(tmp_path):
    """Test is_customized when file content changed."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("original content")

    # Add file with original content
    manifest.add_file(test_file, source="framework:gtd")

    # Modify file
    test_file.write_text("modified content")

    # Should detect customization
    assert manifest.is_customized(test_file) is True


@pytest.mark.unit
def test_manifest_is_customized_hash_unchanged(tmp_path):
    """Test is_customized when file content unchanged."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    # Add file
    manifest.add_file(test_file, source="framework:gtd")

    # No modification
    assert manifest.is_customized(test_file) is False


@pytest.mark.unit
def test_manifest_is_customized_file_missing(tmp_path):
    """Test is_customized when file no longer exists."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    # Add file
    manifest.add_file(test_file, source="framework:gtd")

    # Delete file
    test_file.unlink()

    # Should return False (can't compare hash)
    assert manifest.is_customized(test_file) is False


@pytest.mark.unit
def test_manifest_is_customized_relative_path(tmp_path):
    """Test is_customized with relative paths."""
    manifest = Manifest()
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    test_file = journal_path / "test.md"
    test_file.write_text("original")

    # Add with relative path
    manifest.add_file(test_file, source="framework:gtd", relative_to=journal_path)

    # Modify
    test_file.write_text("modified")

    # Check with absolute path
    assert manifest.is_customized(test_file, relative_to=journal_path) is True


@pytest.mark.unit
def test_manifest_mark_customized(tmp_path):
    """Test marking a file as customized."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    # Add file
    manifest.add_file(test_file, source="framework:gtd", customized=False)

    # Mark as customized
    manifest.mark_customized(test_file)

    assert manifest.files[str(test_file)].customized is True


@pytest.mark.unit
def test_manifest_mark_customized_not_tracked(tmp_path):
    """Test marking untracked file as customized does nothing."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"

    # Should not raise error
    manifest.mark_customized(test_file)

    assert str(test_file) not in manifest.files


@pytest.mark.unit
def test_manifest_update_hash(tmp_path):
    """Test updating file hash."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("original content")

    # Add file
    manifest.add_file(test_file, source="framework:gtd")
    original_hash = manifest.files[str(test_file)].hash

    # Modify file
    test_file.write_text("new content")

    # Update hash
    manifest.update_hash(test_file)

    new_hash = manifest.files[str(test_file)].hash
    assert new_hash != original_hash
    assert manifest.files[str(test_file)].customized is False


@pytest.mark.unit
def test_manifest_update_hash_not_tracked(tmp_path):
    """Test updating hash for untracked file does nothing."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    # Should not raise error
    manifest.update_hash(test_file)

    assert str(test_file) not in manifest.files


@pytest.mark.unit
def test_manifest_update_hash_file_missing(tmp_path):
    """Test updating hash when file doesn't exist."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("test content")

    # Add file
    manifest.add_file(test_file, source="framework:gtd")
    original_hash = manifest.files[str(test_file)].hash

    # Delete file
    test_file.unlink()

    # Update hash (should do nothing)
    manifest.update_hash(test_file)

    # Hash should be unchanged
    assert manifest.files[str(test_file)].hash == original_hash


@pytest.mark.unit
def test_manifest_update_hash_resets_customized_flag(tmp_path):
    """Test that update_hash resets the customized flag."""
    manifest = Manifest()
    test_file = tmp_path / "test.md"
    test_file.write_text("original content")

    # Add and mark as customized
    manifest.add_file(test_file, source="framework:gtd", customized=True)

    # Update hash
    manifest.update_hash(test_file)

    # Customized flag should be reset
    assert manifest.files[str(test_file)].customized is False


@pytest.mark.unit
def test_manifest_get_customized_files(tmp_path):
    """Test getting list of customized files."""
    manifest = Manifest()

    # Add some files
    file1 = tmp_path / "file1.md"
    file1.write_text("content1")
    manifest.add_file(file1, source="framework:gtd", customized=True)

    file2 = tmp_path / "file2.md"
    file2.write_text("content2")
    manifest.add_file(file2, source="framework:gtd", customized=False)

    file3 = tmp_path / "file3.md"
    file3.write_text("content3")
    manifest.add_file(file3, source="system:ide", customized=True)

    # Get all customized files
    customized = manifest.get_customized_files()

    assert len(customized) == 2
    assert str(file1) in customized
    assert str(file3) in customized
    assert str(file2) not in customized


@pytest.mark.unit
def test_manifest_get_customized_files_with_filter(tmp_path):
    """Test getting customized files with source filter."""
    manifest = Manifest()

    # Add files from different sources
    file1 = tmp_path / "file1.md"
    file1.write_text("content1")
    manifest.add_file(file1, source="framework:gtd", customized=True)

    file2 = tmp_path / "file2.md"
    file2.write_text("content2")
    manifest.add_file(file2, source="framework:para", customized=True)

    file3 = tmp_path / "file3.md"
    file3.write_text("content3")
    manifest.add_file(file3, source="system:ide", customized=True)

    # Filter by framework
    framework_customized = manifest.get_customized_files(source_filter="framework:")

    assert len(framework_customized) == 2
    assert str(file1) in framework_customized
    assert str(file2) in framework_customized
    assert str(file3) not in framework_customized


@pytest.mark.unit
def test_manifest_get_customized_files_empty():
    """Test getting customized files when none exist."""
    manifest = Manifest()

    customized = manifest.get_customized_files()

    assert customized == []


@pytest.mark.unit
def test_is_in_safe_zone_ai_instructions(tmp_path):
    """Test that .ai-instructions is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / ".ai-instructions"
    safe_dir.mkdir()
    test_file = safe_dir / "my-coach.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_framework_backups(tmp_path):
    """Test that .framework-backups is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / ".framework-backups"
    safe_dir.mkdir()
    test_file = safe_dir / "backup.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_daily(tmp_path):
    """Test that daily/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "daily"
    safe_dir.mkdir()
    test_file = safe_dir / "2025-01-09.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_projects(tmp_path):
    """Test that projects/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "projects"
    safe_dir.mkdir()
    test_file = safe_dir / "my-project.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_people(tmp_path):
    """Test that people/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "people"
    safe_dir.mkdir()
    test_file = safe_dir / "john-doe.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_memories(tmp_path):
    """Test that memories/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "memories"
    safe_dir.mkdir()
    test_file = safe_dir / "insight.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_areas(tmp_path):
    """Test that areas/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "areas"
    safe_dir.mkdir()
    test_file = safe_dir / "health.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_resources(tmp_path):
    """Test that resources/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "resources"
    safe_dir.mkdir()
    test_file = safe_dir / "reference.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_archive(tmp_path):
    """Test that archive/ is a safe zone."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "archive"
    safe_dir.mkdir()
    test_file = safe_dir / "old-project.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_is_in_safe_zone_root_file_not_safe(tmp_path):
    """Test that files in journal root are not safe."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    test_file = journal_path / "template.md"

    assert is_in_safe_zone(test_file, journal_path) is False


@pytest.mark.unit
def test_is_in_safe_zone_system_dir_not_safe(tmp_path):
    """Test that system directories are not safe."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    system_dir = journal_path / ".cursor"
    system_dir.mkdir()
    test_file = system_dir / "rules.md"

    assert is_in_safe_zone(test_file, journal_path) is False


@pytest.mark.unit
def test_is_in_safe_zone_file_outside_journal(tmp_path):
    """Test that files outside journal are not safe."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    test_file = tmp_path / "other" / "file.md"

    assert is_in_safe_zone(test_file, journal_path) is False


@pytest.mark.unit
def test_is_in_safe_zone_nested_safe_dir(tmp_path):
    """Test that files nested within safe dirs are safe."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()
    safe_dir = journal_path / "projects" / "work" / "2025"
    safe_dir.mkdir(parents=True)
    test_file = safe_dir / "quarterly-goals.md"

    assert is_in_safe_zone(test_file, journal_path) is True


@pytest.mark.unit
def test_manifest_compute_hash_same_content(tmp_path):
    """Test that same content produces same hash."""
    file1 = tmp_path / "file1.md"
    file2 = tmp_path / "file2.md"
    content = "test content\nline 2\nline 3"

    file1.write_text(content)
    file2.write_text(content)

    manifest = Manifest()
    hash1 = manifest._compute_hash(file1)
    hash2 = manifest._compute_hash(file2)

    assert hash1 == hash2


@pytest.mark.unit
def test_manifest_compute_hash_different_content(tmp_path):
    """Test that different content produces different hash."""
    file1 = tmp_path / "file1.md"
    file2 = tmp_path / "file2.md"

    file1.write_text("content 1")
    file2.write_text("content 2")

    manifest = Manifest()
    hash1 = manifest._compute_hash(file1)
    hash2 = manifest._compute_hash(file2)

    assert hash1 != hash2


@pytest.mark.unit
def test_manifest_compute_hash_large_file(tmp_path):
    """Test hash computation for large file."""
    test_file = tmp_path / "large.md"

    # Create a file larger than the chunk size (8192 bytes)
    large_content = "x" * 10000
    test_file.write_text(large_content)

    manifest = Manifest()
    file_hash = manifest._compute_hash(test_file)

    assert file_hash != ""
    assert len(file_hash) == 64  # SHA256 hex digest is 64 characters


@pytest.mark.unit
def test_manifest_add_file_non_relative_path(tmp_path):
    """Test add_file with absolute path that cannot be made relative (lines 99-100)."""
    manifest = Manifest()

    # Create file in a completely different directory
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    other_file = other_dir / "file.txt"
    other_file.write_text("content")

    # Try to make it relative to a different directory
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    # This should trigger the ValueError exception and keep absolute path
    manifest.add_file(other_file, source="test", relative_to=journal_dir)

    # File should be tracked with absolute path (since it couldn't be made relative)
    assert str(other_file) in manifest.files


@pytest.mark.unit
def test_manifest_is_customized_non_relative_path(tmp_path):
    """Test is_customized with absolute path that cannot be made relative (lines 128-129)."""
    manifest = Manifest()

    # Create file in a different directory
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    other_file = other_dir / "file.txt"
    other_file.write_text("original")

    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    # Add file with absolute path
    manifest.add_file(other_file, source="test", relative_to=journal_dir)

    # Modify file
    other_file.write_text("modified")

    # Check if customized - should handle ValueError and still work
    result = manifest.is_customized(other_file, relative_to=journal_dir)

    # Should detect customization despite path not being relative
    assert result is True


@pytest.mark.unit
def test_manifest_mark_customized_non_relative_path(tmp_path):
    """Test mark_customized with absolute path that cannot be made relative (lines 159-162)."""
    manifest = Manifest()

    # Create file in a different directory
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    other_file = other_dir / "file.txt"
    other_file.write_text("content")

    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    # Add file
    manifest.add_file(other_file, source="test", relative_to=journal_dir)

    # Mark as customized - should handle ValueError
    manifest.mark_customized(other_file, relative_to=journal_dir)

    # Check that it was marked
    entry = manifest.files[str(other_file)]
    assert entry.customized is True


@pytest.mark.unit
def test_manifest_update_hash_non_relative_path(tmp_path):
    """Test update_hash with absolute path that cannot be made relative (lines 176-179)."""
    manifest = Manifest()

    # Create file in a different directory
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    other_file = other_dir / "file.txt"
    other_file.write_text("original")

    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()

    # Add file
    manifest.add_file(other_file, source="test", relative_to=journal_dir)
    old_hash = manifest.files[str(other_file)].hash

    # Modify file
    other_file.write_text("modified")

    # Update hash - should handle ValueError
    manifest.update_hash(other_file, relative_to=journal_dir)

    # Hash should be updated
    new_hash = manifest.files[str(other_file)].hash
    assert new_hash != old_hash
