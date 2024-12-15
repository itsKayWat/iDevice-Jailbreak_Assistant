import subprocess
import sys
import os

def install_requirements():
    print("Installing required packages...")
    
    # List of required packages
    requirements = [
        'colorama',
        'requests',
        'pyusb',
        'zipfile36'
    ]
    
    # Install each package
    for package in requirements:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {str(e)}")
            return False
    
    print("\nAll requirements installed successfully!")
    return True

if __name__ == "__main__":
    if os.name != 'nt':
        print("This script is designed for Windows systems only.")
        sys.exit(1)
    
    print("iDeviceJailbreakAssistant Requirements Installer")
    print("=============================================")
    
    if install_requirements():
        print("\nSetup complete! You can now run setup_jailbreak.py")
    else:
        print("\nSetup failed. Please check the errors above and try again.")
    
    input("\nPress Enter to exit...")