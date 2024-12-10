"""The test class TestExampleClassParent is a test class for the class App."""

from python_factory.example import App, factory_for_app


class TestExampleClassParent:
    """The test class for the class App."""

    def application_factory_for_test(self) -> App:
        """Create an application for testing."""
        application: App = factory_for_app()
        return application
