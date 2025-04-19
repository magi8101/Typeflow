import sys
import os
import subprocess
import site

def main():
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path}")
    
    print("\nChecking pip installation...")
    try:
        import pip
        print(f"Pip version: {pip.__version__}")
        print(f"Pip location: {pip.__file__}")
    except ImportError:
        print("Pip not found in the current environment")
    
    print("\nTrying to install setuptools using alternative methods...")
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        print("Successfully ran ensurepip")
    except subprocess.CalledProcessError:
        print("ensurepip failed")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        print("Successfully upgraded pip, setuptools, and wheel")
    except subprocess.CalledProcessError:
        print("Failed to upgrade packages using pip module")
    
    print("\nUser site packages directory:")
    print(site.getusersitepackages())
    
    print("\nTry running your setup with:")
    print(f"{sys.executable} setup.py install --user")
    print("Or:")
    print(f"{sys.executable} -m pip install -e .")

if __name__ == "__main__":
    main()
