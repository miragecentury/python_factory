"""Provides the concrete application class."""

import injector

from python_factory.core.app import BaseApplication, GenericBaseApplicationModule

from ..services.books import BookService
from .config import AppConfig


class App(BaseApplication):
    """Concrete application class."""

    PACKAGE_NAME: str = "python_factory.example"

    def __init__(self, config: injector.Inject[AppConfig]) -> None:
        """Instanciate the application.

        Args:
            config (AppConfig): The application configuration.
        """
        super().__init__(config=config)

        # Prevent circular imports
        from ..api import api_router  # pylint: disable=import-outside-toplevel

        self.get_asgi_app().include_router(router=api_router)


class AppModule(GenericBaseApplicationModule[App, AppConfig]):
    """Configure the injection bindings for the application."""

    def configure(self, binder: injector.Binder) -> None:
        """Configure the injection bindings.

        Args:
            binder (injector.Binder): The injection binder.
        """
        super().configure(binder=binder)

        # Bind Services

        # Book Service as Singleton due to the ClassVar book_store (shared state)
        # It's temporary, we will replace it with a database later
        binder.bind(
            interface=BookService, to=BookService, scope=injector.SingletonScope
        )


def factory_for_app(injector_instance: injector.Injector | None = None) -> App:
    """Provides the application factory.

    TODO: Move this to core and transform it into a generic factory.
    """
    if injector_instance is None:
        injector_instance = injector.Injector()
        injector_instance.binder.install(AppModule)
    application: App = injector_instance.get(interface=App)
    application.attach_injector(injector=injector_instance)
    return application
