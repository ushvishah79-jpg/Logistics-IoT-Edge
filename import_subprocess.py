import subprocess

scripts = [
    "tamper_firmware.py",
    "invalid_signature.py",
    "logger.py",
    "alerts.py"
]

for script in scripts:
    print(f"\nRunning {script}")
    subprocess.run(["python", script])

print("\nAll security tests completed.")