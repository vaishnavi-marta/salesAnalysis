import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PS1_PATH = os.path.join(SCRIPT_DIR, "run_project.ps1")

if not os.path.exists(PS1_PATH):
    print("Error: run_project.ps1 not found in the project directory.")
    sys.exit(1)

try:
    subprocess.check_call([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        PS1_PATH,
    ])
except FileNotFoundError:
    print("Error: PowerShell was not found on this system.")
    print("Run the launcher directly with: .\\run_project.ps1")
    sys.exit(1)
except subprocess.CalledProcessError as exc:
    sys.exit(exc.returncode)
