import subprocess
import os
import sys
import shutil

def run_command(command, show_output=True):
    """Runs a shell command."""
    if show_output:
        print(f"Running: {command}")
    
    # executable='/bin/bash' ensures shell features work
    result = subprocess.run(command, shell=True, executable='/bin/bash')
    
    if result.returncode != 0:
        print(f"Error running command: {command}")
        sys.exit(1)

def setup_virtualenv_workaround():
    """
    Creates venv without pip to bypass missing python3-venv package,
    then manually installs pip. Handles broken existing installs.
    """
    print("\n--- Setting up Virtual Environment ---")
    
    cwd = os.getcwd()
    venv_path = os.path.join(cwd, "redenv")
    pip_check = os.path.join(venv_path, "bin", "pip")
    
    # 1. CLEANUP: Check if folder exists but is broken (missing pip)
    if os.path.exists(venv_path):
        if not os.path.exists(pip_check):
            print(f"Found broken virtualenv at {venv_path}. Deleting and recreating...")
            shutil.rmtree(venv_path)
        else:
            print(f"Directory {venv_path} exists and seems valid. Skipping creation.")
            return venv_path

    # 2. CREATE: venv with --without-pip to avoid the Pterodactyl ensurepip error
    print("Creating venv structure...")
    run_command(f"python3.11 -m venv {venv_path} --without-pip")
    
    # 3. DOWNLOAD: get-pip.py
    print("Downloading get-pip.py...")
    run_command("curl -sL https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    
    # 4. INSTALL: Manually bootstrap pip
    print("Bootstrapping pip...")
    venv_python = os.path.join(venv_path, "bin", "python3.11")
    
    if not os.path.exists(venv_python):
        print(f"CRITICAL ERROR: python3.11 binary not found at {venv_python}")
        sys.exit(1)

    run_command(f"{venv_python} get-pip.py", show_output=False)
    
    # 5. CLEANUP FILE
    if os.path.exists("get-pip.py"):
        os.remove("get-pip.py")
        
    print(f"Virtual environment ready at {venv_path}")
    return venv_path

def install_red(venv_path):
    """Installs Red-DiscordBot using the pip inside the venv."""
    print("\n--- Installing Red-DiscordBot (This may take a moment) ---")
    
    pip_exec = os.path.join(venv_path, "bin", "pip")
    
    if not os.path.exists(pip_exec):
        print(f"Error: Could not find pip at {pip_exec}")
        sys.exit(1)

    # Upgrade pip and wheel
    run_command(f"{pip_exec} install -U pip wheel", show_output=False)
    
    # Install Red
    run_command(f"{pip_exec} install -U Red-DiscordBot")

def run_setup(venv_path):
    """Directly executes redbot-setup."""
    setup_bin = os.path.join(venv_path, "bin", "redbot-setup")
    
    print("\n" + "="*40)
    print("STARTING REDBOT SETUP NOW")
    print("="*40)
    print("Please follow the prompts below to configure your bot instance.\n")
    
    # We use os.system here to ensure the interactive console works perfectly
    os.system(setup_bin)

def main():
    print("--- Pterodactyl Red Installer & Configurator ---")
    
    # Sanity check for Python 3.11
    try:
        subprocess.check_output(["python3.11", "--version"])
    except Exception:
        print("ERROR: python3.11 command not found. Please switch your Pterodactyl Egg.")
        sys.exit(1)

    # 1. Setup Environment
    venv_path = setup_virtualenv_workaround()
    
    # 2. Install Files
    install_red(venv_path)
    
    # 3. Run Setup immediately
    run_setup(venv_path)
    
    # 4. Final Instructions
    print("\n" + "="*40)
    print("SETUP COMPLETE!")
    print("="*40)
    print("Important: To make the server start automatically,")
    print("Go to the PTERODACTYL STARTUP TAB and set 'Startup Command' to:")
    print("-" * 20)
    print(f"source {venv_path}/bin/activate && redbot <your_instance_name>")
    print("-" * 20)
    print("(Replace <your_instance_name> with the name you just chose in the setup)")

if __name__ == "__main__":
    main()