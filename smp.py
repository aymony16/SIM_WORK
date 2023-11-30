# this class will simulate the smartpower board
#                                  _ _ _ _ _ _ _ _ _ out LRAM (ethernet,reset,vg enable) from column
# Power (from POL48V) -- (SMP)  --|
#                                 |_ _ _ _ _ _ _ _ _ out 6smas (J2-J8) for vg biasing sma to dab + hpa

# tests are
# 1 . Power on
# supply 48 volt to smp
# 2. check boot
# veiyfy os is fully bootup
# exceute a grpc command to get version info
# 3.
import time
import json
import threading
from enum import Enum
import paramiko
from dataclasses import dataclass
from smp_service import SmartPowerClient


def load_from_json(filename='smp.json'):
    with open(filename) as f:
        return json.load(f)

########### Petalinux ###############


class Petalinux:
    def __init__(self, attributes) -> None:
        self.__dict__.update(attributes)
        self.ssh_session: paramiko.SSHClient = None
        self.status: PetalinuxStatus = PetalinuxStatus.BOOTING
        self.threads = {}
        self.threads.update(
            {"boot_up": threading.Thread(target=self.__boot_up)})

    def __boot_up(self):
        time.sleep(20)
        SmartPowerClient().check_status()
        self.status = PetalinuxStatus.RUNNING
        print("booted up")

    def update_build(self, build):
        # Todo: add ssh session to get ssh key and then put correct build files then reboot command
        pass

    def __repr__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class PetalinuxStatus(Enum):
    BOOTING = 1
    RUNNING = 2
    ERROR = 3


@dataclass
class SmartPowerSoftware:
    petalinux: Petalinux = ()

    def __repr__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


########### HW ###############
@dataclass
class SmartPowerHardware:
    cpu: str
    pwr_reg: str
    vgs: dict
    lram: dict

    def __repr__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

########### ERROR ###############


class SmartPowerError(Exception):
    LONG_PULSE_ERROR = '0x18;[0]'
    POL_TIMEOUT_ERROR = '0x18;[0]'
    POL_FAULT_ERROR = '0x18;[0]'
    POL_PGOOD_ERROR = '0x18;[0]'

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code


class SmartPowerFPGA:
    def __init__(self, hw, sw) -> None:
        self.hw: SmartPowerHardware = hw
        self.sw: SmartPowerSoftware = sw

    def __repr__(self) -> str:
        return f"SmartPowerFPGA(hw={self.hw}, sw={self.sw})"

    def boot_up(self, delay=1):
        print(f"{self.__class__} booting up")
        self.sw.petalinux.threads["boot_up"].start()
        start_time = time.time()  # Start the timer
        while True:
            if self.sw.petalinux.status == PetalinuxStatus.RUNNING:
                print("booted up")
                break
            elapsed_time = time.time() - start_time  # Calculate the elapsed time
            if elapsed_time > 30:  # Raise an error if it takes longer than 30 seconds
                raise SmartPowerError(
                    "Boot up process took too long.", SmartPowerError.ERROR_CODE_1)
            time.sleep(delay)
            print(f'Checking Petalinux status: {self.sw.petalinux.status}')

    def get_version(self):
        return self.sw.petalinux.version

    @classmethod
    def from_json(cls):
        param = load_from_json()
        hw = SmartPowerHardware(**param['SmartPowerHardware'])
        sw = SmartPowerSoftware(Petalinux(param['SmartPowerSoftware']))
        return cls(hw, sw)


if __name__ == "__main__":
    smp = SmartPowerFPGA.from_json()
    print(smp.hw)
    print(smp.sw)
    smp.boot_up(2)
    print("done")
