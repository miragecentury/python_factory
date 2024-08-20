"""Python Factory Example."""

from python_factory.core.app.utils import UvicornUtils
from python_factory.core.utils.log import LogModeEnum, setup_log
from python_factory.example.app import App, factory_for_app


def application_factory() -> App:
    """Provides the application factory."""
    return factory_for_app()


def main() -> None:
    """Main function."""
    setup_log(mode=LogModeEnum.CONSOLE)
    application: App = application_factory()
    uvicorn_utils = UvicornUtils(app=application, config=application.get_config())

    try:
        uvicorn_utils.serve()
    except KeyboardInterrupt:
        pass
