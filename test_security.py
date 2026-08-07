import subprocess

tests = [
    "tamper_firmware.py",
    "invalid_signature.py",
    "logger.py",
    "alerts.py"
]

for test in tests:
    print(f"\nRunning {test}")
    subprocess.run(["python", test])