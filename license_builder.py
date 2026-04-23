import os

def create_license_kit():
    print("===========================================")
    print("     MASTER LICENSE KIT GENERATOR          ")
    print("===========================================")
    
    app_name = input("Enter the Software Name (e.g., Inventory Pro): ").strip()
    salt = input("Enter a UNIQUE Secret Salt: ").strip()
    
    # Create a clean folder name
    folder_name = f"{app_name.replace(' ', '_')}_License_Kit"
    os.makedirs(folder_name, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. TEMPLATE FOR KEYGEN.PY (With Auto/Manual Feature)
    # ---------------------------------------------------------
    keygen_code = f"""import subprocess
import hashlib
import sys
from datetime import datetime, timedelta

SECRET_SALT = "{salt}"
APP_NAME = "{app_name}"

def get_local_hwid():
    try:
        print("Fetching Local Hardware ID...")
        return subprocess.check_output(
            ["powershell", "-Command", "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"],
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode().strip()
    except Exception as e:
        print("Error reading local hardware ID:", e)
        sys.exit(1)

def generate_license():
    print("=======================================")
    print(f"   {{APP_NAME}} KEY GENERATOR")
    print("=======================================")
    print("1. Auto Mode   (Generate for THIS computer)")
    print("2. Manual Mode (Generate for a REMOTE client)")
    
    mode = input("\\nSelect mode (1 or 2): ").strip()
    
    if mode == '1':
        hwid = get_local_hwid()
        print(f"\\n[+] Local HWID: {{hwid}}")
    elif mode == '2':
        hwid = input("\\nEnter the remote client's HWID: ").strip()
        if not hwid: return
    else:
        return

    print("\\n--- LICENSE DURATION ---")
    print("1. Days\\n2. Weeks\\n3. Months\\n4. Years\\n5. Lifetime")
    
    choice = input("\\nSelect duration (1-5): ").strip()
    
    if choice == '5':
        expiry_str = "9999-12-31"
    else:
        try:
            amount = int(input("Enter number: ").strip())
            days = amount if choice == '1' else amount * 7 if choice == '2' else amount * 30 if choice == '3' else amount * 365
            expiry_str = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        except ValueError:
            return

    signature = hashlib.sha256((hwid + expiry_str + SECRET_SALT).encode()).hexdigest()
    
    with open("license.key", "w") as f:
        f.write(f"{{expiry_str}}:{{signature}}")
        
    print(f"\\n[SUCCESS] license.key generated for {{APP_NAME}}!")
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    generate_license()
"""

    # ---------------------------------------------------------
    # 2. TEMPLATE FOR LICENSE_CHECKER.PY
    # ---------------------------------------------------------
    checker_code = f"""import subprocess
import hashlib
import os
import sys
from datetime import datetime

SECRET_SALT = "{salt}"
APP_NAME = "{app_name}"

def get_hwid():
    try:
        return subprocess.check_output(
            ["powershell", "-Command", "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"],
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode().strip()
    except Exception as e:
        print("Error reading hardware ID:", e)
        input("Press Enter to exit...")
        sys.exit(1)

def verify_license():
    hwid = get_hwid()
    license_file = "license.key"
    
    if not os.path.exists(license_file):
        print("NO LICENSE FOUND!")
        print(f"Your HWID is: {{hwid}}")
        print("Contact the developer to purchase a license.")
        input("Press Enter to exit...")
        sys.exit(1) 
        
    with open(license_file, "r") as f:
        content = f.read().strip()
        
    if ":" not in content:
        print("CORRUPTED LICENSE KEY!")
        sys.exit(1)
        
    expiry_str, provided_signature = content.split(":", 1)
    expected_signature = hashlib.sha256((hwid + expiry_str + SECRET_SALT).encode()).hexdigest()
    
    if provided_signature != expected_signature:
        print("INVALID LICENSE KEY!")
        input("Press Enter to exit...")
        sys.exit(1) 
        
    if expiry_str != "9999-12-31":
        if datetime.now() > datetime.strptime(expiry_str, "%Y-%m-%d"):
            print(f"LICENSE EXPIRED on {{expiry_str}}!")
            input("Press Enter to exit...")
            sys.exit(1)

    print(f"{{APP_NAME}} License Verified. Starting system...")
"""

    # ---------------------------------------------------------
    # 3. TEMPLATE FOR INSTRUCTIONS.TXT
    # ---------------------------------------------------------
    instructions_code = f"""INTEGRATION GUIDE FOR: {app_name}

STEP 1: Move Files
Move the 'license_checker.py' file into the same folder as your main app.py file.

STEP 2: Update app.py
Open your app.py file and put this import at the very top of the file:
from license_checker import verify_license

STEP 3: Trigger the check
Scroll to the very bottom of your app.py where the server starts, and add verify_license() BEFORE your app runs.

Example:
if __name__ == "__main__":
    verify_license()
    app.run(host="0.0.0.0", port=5000)

STEP 4: Compile
When you compile your new software, don't forget to compile the keygen too!
python -m PyInstaller --name "{app_name.replace(' ', '_')}_Keygen" --onefile keygen.py
"""

    # ---------------------------------------------------------
    # WRITE THE FILES TO THE NEW FOLDER
    # ---------------------------------------------------------
    with open(os.path.join(folder_name, "keygen.py"), "w") as f:
        f.write(keygen_code)
        
    with open(os.path.join(folder_name, "license_checker.py"), "w") as f:
        f.write(checker_code)
        
    with open(os.path.join(folder_name, "instructions.txt"), "w") as f:
        f.write(instructions_code)
        
    print(f"\n[SUCCESS] Custom License Kit created in folder: {folder_name}")

if __name__ == "__main__":
    create_license_kit()