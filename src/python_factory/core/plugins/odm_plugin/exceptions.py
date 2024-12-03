"""Provides the exceptions for the ODM_Plugin."""


class ODMPluginBaseException(BaseException):
    """Base exception for the ODM_Plugin."""

    pass


class ODMPluginConfigError(ODMPluginBaseException):
    """Exception for the ODM_Plugin configuration."""

    pass
