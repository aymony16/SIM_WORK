import pytest
from smp import SmartPowerFPGA, PetalinuxStatus, SmartPowerError


@pytest.fixture
def petalinux_mock(mocker):
    petalinux_mock = mocker.Mock()
    petalinux_mock.threads = {"boot_up": mocker.Mock(start=mocker.Mock())}
    return petalinux_mock


@pytest.fixture
def sw_mock(petalinux_mock, mocker):
    sw_mock = mocker.Mock()
    sw_mock.petalinux = petalinux_mock
    return sw_mock


@pytest.mark.parametrize(
    "status, delay, expected_exception",
    [
        (PetalinuxStatus.RUNNING, 1, None),
        (PetalinuxStatus.NOT_RUNNING, 0.01, SmartPowerError),
    ],
)
def test_boot_up(sw_mock, status, delay, expected_exception):
    # Set the status of the petalinux mock
    sw_mock.petalinux.status = status

    # Create a SmartPowerFPGA instance with the sw mock
    spfpga = SmartPowerFPGA(sw=sw_mock)

    # Test the boot_up method
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            spfpga.boot_up(delay=delay)
    else:
        spfpga.boot_up(delay=delay)

    # Verify that the boot_up thread was started
    sw_mock.petalinux.threads["boot_up"].start.assert_called_once()
