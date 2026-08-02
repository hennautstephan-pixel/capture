from capture_recovery.recovery import IntegritySeverity


def test_is_fatal():

    assert IntegritySeverity.CRITICAL.is_fatal is True

    assert IntegritySeverity.ERROR.is_fatal is False


def test_is_error():

    assert IntegritySeverity.ERROR.is_error is True

    assert IntegritySeverity.CRITICAL.is_error is True

    assert IntegritySeverity.WARNING.is_error is False

    assert IntegritySeverity.INFO.is_error is False