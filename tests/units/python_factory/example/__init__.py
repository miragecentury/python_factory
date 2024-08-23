"""The test class TestExampleClassParent is a test class for the class App."""

import injector

from python_factory.core.plugins.opentelemetry_plugin.configs import OpenTelemetryConfig
from python_factory.example import App, AppModule, application_factory


class TestExampleClassParent:
    """The test class for the class App."""

    def binder_configure(self, binder: injector.Binder) -> None:
        """Configure the binder for the test."""
        binder.bind(
            interface=OpenTelemetryConfig, to=OpenTelemetryConfig(activate=False)
        )

    def application_factory_for_test(self) -> App:
        """Create an application for testing."""
        injector_instance = injector.Injector()
        injector_instance.binder.install(module=AppModule)
        self.binder_configure(injector_instance.binder)
        application: App = application_factory(injector_instance=injector_instance)

        return application
