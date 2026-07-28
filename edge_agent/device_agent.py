import os

from logger import (
    log_info,
    log_warning,
    log_success,
    log_critical
)

from verifier import verify_firmware

from installer import (
    install_firmware,
    update_installed_version,
    reboot_device
)


class EdgeDeviceAgent:

    def __init__(self):

        self.device_id = "EDGE_DEVICE_001"

        self.current_version = "0.0.0"


    def start_ota_update(self):

        log_info("=" * 50)
        log_info(f"{self.device_id} : OTA Update Started")
        log_info("=" * 50)

        # Step 1 : Verify firmware

        if verify_firmware():

            log_success("Firmware verification successful.")

            # Step 2 : Install firmware

            install_firmware()

            # Step 3 : Update installed version

            self.current_version = "1.0.0"

            update_installed_version(self.current_version)

            # Step 4 : Reboot

            reboot_device()

            log_success("=" * 50)
            log_success("OTA UPDATE COMPLETED SUCCESSFULLY")
            log_success("=" * 50)

            print("\nSTATUS : UPDATE SUCCESSFUL")

            return True

        else:

            log_critical("Firmware verification failed.")

            log_warning("Firmware installation aborted.")

            print("\nSTATUS : UPDATE BLOCKED")

            return False


if __name__ == "__main__":

    print("\n" + "=" * 50)
    print(" Edge Device OTA Agent ")
    print("=" * 50)

    device = EdgeDeviceAgent()

    device.start_ota_update()