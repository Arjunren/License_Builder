# License_Builder
An automated licensing toolkit for software protection. Generates hardware-locked (HWID) key generators and verification scripts using SHA-256 hashing and unique secret salts to prevent unauthorized software distribution.

# 🔑 Master License Kit Generator

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-SHA--256-green?logo=google-cloud&logoColor=white)](https://en.wikipedia.org/wiki/SHA-2)
[![PyInstaller](https://img.shields.io/badge/Build-PyInstaller-blue)](https://pyinstaller.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Master License Kit Generator** is a professional-grade utility designed for software developers who need to implement hardware-locked licensing for their applications. It generates a complete protection suite—including a key generator, a license checker, and integration instructions—customized with your unique security salt.

---

## ✨ Key Features

### 🛡️ Hardware-Locked Security
* **HWID Binding:** Licenses are tied to the unique Windows UUID (Hardware ID), preventing keys from being shared between different computers.
* **SHA-256 Hashing:** Uses high-security cryptographic hashing combined with a unique "Secret Salt" to prevent license tampering or forgery.
* **Tamper Detection:** Built-in verification logic checks for corrupted or modified license files.

### 🕒 Flexible License Management
* **Auto & Manual Modes:** Generate keys for the local machine instantly or create keys for remote clients using their provided HWID.
* **Granular Expiration:** Set license durations in Days, Weeks, Months, or Years.
* **Lifetime Support:** Option to generate permanent, non-expiring licenses.

### 🛠️ Developer Integration
* **Automated Kit Generation:** Creates a clean, organized folder containing everything needed to protect your software.
* **Boilerplate Logic:** Includes a ready-to-use `license_checker.py` that can be imported into any Python application with two lines of code.

---

## 🚀 Getting Started

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Arjunren/License_Builder.git
    cd License_Builder
    ```

2.  **Run the Generator:**
    ```bash
    python license_builder.py
    ```

### Using the Kit
1.  **Enter Configuration:** Provide your Software Name and a **Unique Secret Salt**.
2.  **Locate Output:** Find your custom kit in the generated `[SoftwareName]_License_Kit` folder.
3.  **Integrate:** Follow the generated `instructions.txt` to add `verify_license()` to your application's main entry point.

---

## ⚙️ Compilation Guide

To ensure your licensing system is secure, you should compile the generated `keygen.py` into a standalone executable. Use the following command:

```bash
python -m PyInstaller --name "[SoftwareName]_Keygen" --onefile keygen.py
