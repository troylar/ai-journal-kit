"""CLI entrypoint for AI Journal Kit."""


def main():
    """Main CLI entrypoint."""
    from ai_journal_kit.cli.app import app

    app()


if __name__ == "__main__":
    main()
