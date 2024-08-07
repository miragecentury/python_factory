"""
Provides the concrete application class.
"""

import injector

from python_factory.core.app import AppBase, EnvironmentEnum

from .config import AppConfig


class App(AppBase):
    """
    Concrete application class.
    """

    def __init__(self, config: injector.Inject[AppConfig]) -> None:
        super().__init__(config=config)


class AppInjectorModule(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(App, to=App)

    @injector.singleton
    @injector.provider
    def app_config_provider(self) -> AppConfig:
        return AppConfig(
            environment=EnvironmentEnum.DEVELOPMENT,
        )


def app_factory() -> App:
    """
    Provides the application factory.
    """
    return injector.Injector(modules=[AppInjectorModule]).get(interface=App)
