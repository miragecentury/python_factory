"""
Provides the concrete application class.
"""

import injector

from python_factory.core.app import AppBase
from python_factory.core.app.abstracts import GenericAppModule
from python_factory.core.utils.importlib import get_path_file_in_package
from python_factory.core.utils.yaml_reader import YamlFileReader

from .config import AppConfig


class App(AppBase):
    """
    Concrete application class.
    """

    PACKAGE_NAME: str = "python_factory.example"

    def __init__(self, config: injector.Inject[AppConfig]) -> None:
        super().__init__(config=config)


class AppModule(GenericAppModule[App, AppConfig]):

    @injector.singleton
    @injector.provider
    def provider_for_app_config(self) -> AppConfig:
        return AppConfig(
            **YamlFileReader(
                file_path=get_path_file_in_package(
                    filename="application.yaml", package=App.PACKAGE_NAME
                ),
                yaml_base_key="application",
                use_environment_injection=True,
            ).read()
        )


def app_factory() -> App:
    """
    Provides the application factory.
    """
    return injector.Injector(modules=[AppModule]).get(interface=App)
