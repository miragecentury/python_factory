"""
Main entry point for the application.
"""

from python_factory.core.app.utils import UvicornUtils
from python_factory.core.utils.log import LogModeEnum, setup_log
from python_factory.example.app import App, app_factory


def main():
    setup_log(mode=LogModeEnum.CONSOLE)
    application: App = app_factory()
    uvicorn_utils = UvicornUtils(app=application, config=application.get_config())

    try:
        uvicorn_utils.serve()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
