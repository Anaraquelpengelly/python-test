#!/usr/bin/env python3
import ctypes
import os
import platform
import subprocess
import sys
from shutil import rmtree, which

import colorama


# Platform indepent way to check if user is admin
def is_user_admin():
    """
    Check if the script is being run as root/admin

    Return False if privileges cannot be determined
    """
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        except WindowsError:
            return False

    else:
        try:
            return os.getuid() == 0
        except os.Error:
            return False


# Uninstall Pip packages in a platform independent way
def uninstall_pip_packages():
    """Remove pip packages installed by pygoat"""
    print(colorama.Back.CYAN + colorama.Style.BRIGHT + "[+] Uninstalling Pip packages!" + colorama.Style.RESET_ALL)

    try:
        # It is important to upgrade pip first to avoid environment errors
        if (platform.system() != 'Windows'):
            pip_v = "pip3" if (which('pip3') is not None) else "pip"
            subprocess.run([pip_v,
                            "install",
                            "--upgrade",
                            "pip"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           shell=False)
        
        packages_to_uninstall = []
        try:
            with open("requirements.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                        packages_to_uninstall.append(package_name)
            
            if packages_to_uninstall:
                subprocess.check_call([sys.executable,
                                       "-m",
                                       "pip",
                                       "uninstall",
                                       "-y"] + packages_to_uninstall,
                                      shell=False)
            else:
                print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "[!] No packages found in requirements.txt to uninstall." + colorama.Style.RESET_ALL)

        except FileNotFoundError:
            print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "[!] requirements.txt not found. Skipping package uninstallation." + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[!] An error occurred during package uninstallation: {e}" + colorama.Style.RESET_ALL)

    except subprocess.CalledProcessError:
        print(colorama.Fore.RED + colorama.Style.BRIGHT + "[!] Failed to uninstall pip packages" + colorama.Style.RESET_ALL)


# Uninstall PIP
def uninstall_pip():
    """Remove Pip"""
    print(colorama.Back.RED + colorama.Style.BRIGHT + "[+] Uninstalling Pip!" + colorama.Style.RESET_ALL)
    try:
        subprocess.check_call([sys.executable,
                               "-m",
                               "pip",
                               "uninstall",
                               "-y",
                               "pip"],
                              shell=False)
    except subprocess.CalledProcessError:
        print(colorama.Fore.RED + colorama.Style.BRIGHT + "[!] Failed to uninstall pip" + colorama.Style.RESET_ALL)


# Remove pygoat
def remove_pygoat():
    """Remove pygoat files"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(colorama.Back.RED + colorama.Style.BRIGHT + f"All files in {script_dir} will be deleted!" + colorama.Style.RESET_ALL)

    for item in list(os.listdir(script_dir)):
        if item == os.path.basename(__file__):
            continue

        filename = os.path.join(script_dir, item)

        if os.path.isfile(filename):
            try:
                print("[!] Deleted: " + colorama.Fore.RED + colorama.Style.BRIGHT + filename + colorama.Style.RESET_ALL)
                os.remove(filename)
            except os.Error as e:
                print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[!] Failed To remove file: {filename} - {e}" + colorama.Style.RESET_ALL)
                pass

        elif os.path.isdir(filename):
            try:
                print("[!] Deleted: " + colorama.Fore.RED + colorama.Style.BRIGHT + filename + colorama.Style.RESET_ALL)
                rmtree(filename, ignore_errors=True)
            except Exception as e:
                print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[!] Failed To remove directory: {filename} - {e}" + colorama.Style.RESET_ALL)
                pass


def main():
    colorama.init()

    # Check if program is being run as admin
    # However, you need admin privileges only if you are not in a venv
    if not is_user_admin() and sys.prefix == sys.base_prefix:
        print(colorama.Fore.RED + colorama.Style.BRIGHT +
              "[!] This script requires administrator/root privileges to run outside a virtual environment." + colorama.Style.RESET_ALL)
        sys.exit(1)

    uninstall_pip_packages()
    uninstall_pip()
    remove_pygoat()

    print(colorama.Back.GREEN + colorama.Style.BRIGHT + "[+] Pygoat uninstallation complete!" + colorama.Style.RESET_ALL)

if __name__ == "__main__":
    main()