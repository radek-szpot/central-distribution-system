import os
import subprocess
import sys


def create_virtual_environment(venv_path):
    """
    Create a virtual environment using venv.
    :param venv_path: Path to the virtual environment directory.
    """
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)


def activate_virtual_environment(venv_path):
    """
    Activate the virtual environment.
    :param venv_path: Path to the virtual environment directory.
    """
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")

    subprocess.run(activate_script, shell=True, check=True)


def install_dependencies():
    """
    Install project dependencies using pip.
    """
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)


if __name__ == "__main__":
    current_venv_path = os.path.join(os.getcwd(), "venv")
    create_virtual_environment(current_venv_path)
    activate_virtual_environment(current_venv_path)
    install_dependencies()
    subprocess.run([sys.executable, "app.py"])
