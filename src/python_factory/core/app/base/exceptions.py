"""
Provides the exceptions for the application factory.
"""


class BaseApplicationException(BaseException):
    pass


class ApplicationFactoryException(BaseApplicationException):
    pass


class ApplicationConfigFactoryException(BaseApplicationException):
    pass


class ApplicationPluginManagerException(BaseApplicationException):
    pass
