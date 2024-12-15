import os
import subprocess
import platform
import requests
import time
from colorama import init, Fore, Style
import sys
import zipfile
import usb.core
import usb.util

# Initialize colorama
init()

class DeviceInfo:
    def __init__(self):
        self.device_type = None
        self.ios_version = None
        self.model = None

def print_header():
    print(f"{Fore.CYAN}================================")
    print("JailBreak Setup Assistant")
    print("================================" + Style.RESET_ALL)

def print_step(step_num, total_steps, message):
    print(f"\n{Fore.GREEN}[Step {step_num}/{total_steps}] {message}{Style.RESET_ALL}")

def print_status(message):
    print(f"{Fore.YELLOW}→ {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def detect_ios_device():
    try:
        # Apple's vendor ID
        APPLE_VID = 0x05ac
        
        # Find all Apple devices
        device = usb.core.find(idVendor=APPLE_VID)
        
        if device is None:
            return None
        
        device_info = DeviceInfo()
        
        # Get device information
        try:
            device_info.model = usb.util.get_string(device, device.iProduct)
            # You would need to implement proper iOS version detection here
            # This might require additional libraries or methods
            device_info.ios_version = "Unknown"
            device_info.device_type = "iOS Device"
            return device_info
        except:
            return None
            
    except Exception as e:
        print_error(f"Error detecting device: {str(e)}")
        return None

def wait_for_device():
    print_status("Waiting for iOS device connection...")
    while True:
        device = detect_ios_device()
        if device:
            print_success(f"Device detected: {device.model}")
            return device
        time.sleep(2)

def download_file(url, output_path, description):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print_status(f"Downloading {description}...")
        response = requests.get(url, stream=True, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            
            with open(output_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    file.write(data)
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        sys.stdout.write(f"\rProgress: {percent}% [{downloaded}/{total_size} bytes]")
                        sys.stdout.flush()
            print("\n")
            print_success(f"Downloaded: {description}")
            return True
        else:
            print_error(f"Failed to download {description}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error downloading {description}: {str(e)}")
        return False

def get_jailbreak_url(device_info):
    # Add logic to determine correct jailbreak tool based on device and iOS version
    # This is a simplified example
    if device_info.ios_version.startswith("15"):
        return "https://unc0ver.dev/downloads/8.0.2/9e44edfbfd1905cadf23c3b9ad1d5bed683ce061/unc0ver_Release_8.0.2.ipa"
    else:
        return "https://example.com/other-jailbreak.ipa"

def automate_setup():
    total_steps = 6
    current_step = 1
    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)

    print_header()
    print("\nThis assistant will guide you through the jailbreak setup process.")
    print("Please follow the on-screen instructions carefully.\n")

    # Step 1: Device Detection
    print_step(current_step, total_steps, "Detecting iOS Device")
    print_status("Please connect your iOS device to continue...")
    device_info = wait_for_device()
    if not device_info:
        print_error("No iOS device detected. Please connect your device and try again.")
        return
    current_step += 1

    # Step 2: Prerequisites Check
    print_step(current_step, total_steps, "Checking Prerequisites")
    # Add checks for iTunes and iCloud here
    current_step += 1

    # Step 3: Download AltServer
    print_step(current_step, total_steps, "Downloading AltServer")
    altserver_url = "https://f000.backblazeb2.com/file/altstore/altinstaller.zip"
    altserver_file = os.path.join(downloads_dir, "altinstaller.zip")
    if not download_file(altserver_url, altserver_file, "AltServer"):
        return
    current_step += 1

    # Step 4: Install AltServer
    print_step(current_step, total_steps, "Installing AltServer")
    try:
        with zipfile.ZipFile(altserver_file, 'r') as zip_ref:
            zip_ref.extractall(downloads_dir)
        print_success("AltServer extracted successfully")
    except Exception as e:
        print_error(f"Error extracting AltServer: {str(e)}")
        return
    current_step += 1

    # Step 5: Download Jailbreak Tool
    print_step(current_step, total_steps, "Downloading Jailbreak Tool")
    jailbreak_url = get_jailbreak_url(device_info)
    jailbreak_file = os.path.join(downloads_dir, "jailbreak.ipa")
    if not download_file(jailbreak_url, jailbreak_file, "Jailbreak Tool"):
        return
    current_step += 1

    # Step 6: Final Instructions
    print_step(current_step, total_steps, "Final Setup Instructions")
    print("\nPlease follow these steps to complete the jailbreak:")
    print("1. Launch AltServer from the downloads folder")
    print("2. Make sure your device is still connected")
    print("3. Trust your computer on your iOS device if prompted")
    print("4. Install the jailbreak IPA using AltServer")
    print("5. Launch the jailbreak app on your device")
    print("\nNeed help? Visit our support forum for assistance.")

if __name__ == "__main__":
    if platform.system() != "Windows":
        print_error("This script is only designed for Windows systems.")
    else:
        try:
            automate_setup()
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
        
        input("\nPress Enter to exit...")
