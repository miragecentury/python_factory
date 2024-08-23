"""Python Factory Example."""

import injector

from python_factory.core.app.utils import UvicornUtils
from python_factory.core.utils.log import LogModeEnum, setup_log
from python_factory.example.app import App, AppModule, factory_for_app


def application_factory(injector_instance: injector.Injector | None = None) -> App:
    """Provides the application factory."""
    return factory_for_app(injector_instance=injector_instance)


def main() -> None:
    """Main function."""
    setup_log(mode=LogModeEnum.JSON)
    application: App = application_factory()
    uvicorn_utils = UvicornUtils(app=application, config=application.get_config())

    try:
        uvicorn_utils.serve()
    except KeyboardInterrupt:
        pass


__all__: list[str] = ["App", "application_factory", "main", "AppModule"]
