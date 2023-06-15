from shoshin.__about__ import __version__ as VERSION
from shoshin.exceptions import TroubleshootingExceptionMixin


def test_troubleshooting_exception_mixin_with_code():
    # Ensure TroubleshootingExceptionMixin returns a troubleshooting page if a code is available.
    exception = TroubleshootingExceptionMixin("Processor error", 42)
    # Check
    assert exception.message == "Processor error"
    assert exception.code == 42
    assert (
        str(exception)
        == f"Processor error\n\nTo troubleshoot visit https://github.com/palazzem/shoshin/wiki/{VERSION}-42"
    )


def test_troubleshooting_exception_mixin_without_code():
    # Ensure TroubleshootingExceptionMixin returns the error message if the code is not available.
    exception = TroubleshootingExceptionMixin("Processor error")
    # Check
    assert exception.message == "Processor error"
    assert exception.code is None
    assert str(exception) == "Processor error"
