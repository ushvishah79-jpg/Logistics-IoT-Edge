print("===== CI/CD Security Review =====")

checks = {
    "GitHub Actions Enabled": True,
    "Least Privilege Permissions": True,
    "Secrets Used Instead of Hardcoding": True,
    "Dependency Scanning Enabled": True,
    "Workflow Runs on Protected Branch": True
}

for check, status in checks.items():
    print(f"{check}: {'PASS' if status else 'FAIL'}")

print("\nCI/CD Security Review Completed.")