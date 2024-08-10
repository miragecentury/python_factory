"""
Provides the concrete application class.
"""

import injector

from python_factory.core.app import BaseApplication, GenericBaseApplicationModule

from .config import AppConfig


class App(BaseApplication):
    """
    Concrete application class.
    """

    PACKAGE_NAME: str = "python_factory.example"

    def __init__(self, config: injector.Inject[AppConfig]) -> None:
        super().__init__(config=config)


class AppModule(GenericBaseApplicationModule[App, AppConfig]):
    pass


def factory_for_app() -> App:
    """
    Provides the application factory.
    """
    injector_instance = injector.Injector(modules=[AppModule])
    return injector_instance.get(interface=App)
