"""Python Factory Example."""

from python_factory.example.app import App


def main() -> None:
    """Main function."""
    App.main()


__all__: list[str] = ["App", "main"]
