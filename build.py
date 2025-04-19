import os
import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def main():
    # Get Python executable path
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    
    # Try to install required packages
    run_command(f'"{python_exe}" -m pip install --upgrade pip setuptools wheel')
    
    # Try to build the package
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not run_command(f'"{python_exe}" setup.py sdist bdist_wheel'):
        print("Failed to build with setup.py directly. Trying alternative method...")
        run_command(f'"{python_exe}" -m pip install build')
        run_command(f'"{python_exe}" -m build')
    
    print("Build script completed")

if __name__ == "__main__":
    main()
