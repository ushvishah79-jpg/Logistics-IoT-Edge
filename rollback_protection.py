class RollbackProtection:
    def __init__(self, current_version, new_version):
        self.current_version = current_version
        self.new_version = new_version

    def check_version(self):
        print("===== Rollback Protection =====")
        print("Current Version :", self.current_version)
        print("New Version     :", self.new_version)

        if self.new_version >= self.current_version:
            print("Result : Update Allowed")
        else:
            print("Result : Rollback Detected - Update Blocked")

def main():
    firmware = RollbackProtection(1.0, 1.1)
    firmware.check_version()

if __name__== "__main__":
    main()