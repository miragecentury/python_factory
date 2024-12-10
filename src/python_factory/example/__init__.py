"""Python Factory Example."""

from python_factory.core.app.utils import UvicornUtils
from python_factory.core.utils.log import LogModeEnum, setup_log
from python_factory.example.app import App, factory_for_app


def main() -> None:
    """Main function.

    TODO: Relocate some behavior to the core package.
    This must be the same for all applications.
    """
    setup_log(mode=LogModeEnum.CONSOLE)
    application: App = factory_for_app()
    uvicorn_utils = UvicornUtils(app=application, config=application.get_config())

    try:
        uvicorn_utils.serve()
    except KeyboardInterrupt:
        pass


__all__: list[str] = ["App", "main"]
