from datetime import datetime

class SecureUpdateLog:
    def _init_(self, firmware):
        self.firmware = firmware

    def create_log(self):
        print("===== Secure Update Log =====")
        print("Firmware :", self.firmware)
        print("Status   : Update Successful")
        print("Time     :", datetime.now())
        print("Log Saved Successfully")

def main():
    log = SecureUpdateLog