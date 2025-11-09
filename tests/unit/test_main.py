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


def test_main_as_module():
    """Test executing module with python -m (covers line 12)."""
    with patch("ai_journal_kit.cli.app.app") as mock_app:
        # Read the __main__.py file and execute it with __name__ == "__main__"
        import pathlib

        main_file = pathlib.Path(__file__).parent.parent.parent / "ai_journal_kit" / "__main__.py"
        code = compile(main_file.read_text(encoding="utf-8"), str(main_file), "exec")

        # Execute with __name__ set to "__main__" to trigger the if block
        exec(code, {"__name__": "__main__"})

        # The main() function should have been called
        mock_app.assert_called_once()
