"""
Test the setup.log module
"""

from unittest.mock import patch

from python_poetry_empty.setup.log import setup_log


class TestSetupLog:
    """
    Various tests for the setup_log function
    """

    @patch("structlog.configure")
    def test_structlog_has_been_configured(self, structlog_configure_mock):
        """
        Test that structlog has been configured
        """

        setup_log()

        # Called once and only once
        assert structlog_configure_mock.called
        assert structlog_configure_mock.call_count == 1
