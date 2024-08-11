"""
Provides the exceptions for the OpenTelemetryPlugin.
"""


class OpenTelemetryPluginBaseException(BaseException):
    pass


class OpenTelemetryPluginConfigError(OpenTelemetryPluginBaseException):
    pass
