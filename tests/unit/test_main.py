"""Unit tests for __main__.py entrypoint."""

from unittest.mock import patch


def test_main_calls_app():
    """Test main() function imports and calls app."""
    with patch("ai_journal_kit.cli.app.app") as mock_app:
        from ai_journal_kit.__main__ import main

        main()
        mock_app.assert_called_once()


def test_main_module_execution():
    """Test __main__ module can be executed."""
    # Import should not raise
    import ai_journal_kit.__main__  # noqa: F401

