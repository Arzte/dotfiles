#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Common functions to get TeamSpeak 3 paths from the Windows registry
#

import _winreg, os

#
# Attempt to open TeamSpeak 3 Client registry key in "Software\TeamSpeak 3 Client" for 32 or 64 bit client
# versions in local or global installation mode
#
def openTS3ClientKey(isLocal, is64Bit):
	if isLocal:
		key = _winreg.HKEY_CURRENT_USER
	else:
		key = _winreg.HKEY_LOCAL_MACHINE
	if is64Bit:
		sam = _winreg.KEY_WOW64_64KEY
	else:
		sam = _winreg.KEY_WOW64_32KEY
	try:
		hKey = _winreg.OpenKey(key, r'Software\TeamSpeak 3 Client', 0, _winreg.KEY_READ | sam)
		return hKey
	except WindowsError:
		return None

#
# Try to open the "Software\TeamSpeak 3 Client" registry key
# Depending if the installation is a 32 or 64 bit client and if it was installed locally or into C:\Program Files, there
# we have to try multiple combination to find the right registry location
#
def getTS3ClientHKey():
	hKey = openTS3ClientKey(False, False)  # 32-bit in HKEY_LOCAL_MACHINE
	if not hKey:
		hKey = openTS3ClientKey(True, False)  # 32-bit in HKEY_CURRENT_USER
		if not hKey:
			hKey = openTS3ClientKey(False, True)  # 64-bit in HKEY_LOCAL_MACHINE
			if not hKey:
				hKey = openTS3ClientKey(True, True)  # 64-bit in HKEY_CURRENT_USER
	return hKey

#
# Open TeamSpeak 3 Client registry key and return the value of the given subkey
#
def getTS3ClientRegistryKey(subkey):
	hKey = getTS3ClientHKey()
	if not hKey:
		return None  # Failed
	try:
		value, type = _winreg.QueryValueEx(hKey, subkey)
	except WindowsError, err:
		print 'Failed to find TeamSpeak 3 Client registry key:', err
		_winreg.CloseKey(hKey)
		return None
	_winreg.CloseKey(hKey)
	return value
	
#
# Get TeamSpeak 3 client installation folder from Windows registry
#
def getTS3ClientInstallPath():
	return getTS3ClientRegistryKey('')  # Default key

#
# Get TeamSpeak 3 client binary path
# First get the installation folder from registry, then check for both 32 and 64 bit binary.
# Return full path of the TS3 client binary or None if client was not found.
#
def getTS3ClientBinaryPath():
	installPath = getTS3ClientInstallPath()
	if not installPath:
		return None
	binaryPath = installPath + r'\ts3client_win32.exe'
	if os.path.exists(binaryPath) and os.path.isfile(binaryPath):
		return binaryPath
	binaryPath = getTS3ClientInstallPath() + '\\ts3client_win64.exe'
	if os.path.exists(binaryPath) and os.path.isfile(binaryPath):
		return binaryPath
	return None

#
# Get TeamSpeak 3 client config folder from Windows registry
# Returns full path to the config folder or None if config folder was not found.
#
def getTS3ClientConfigPath():
	configLocation = getTS3ClientRegistryKey('ConfigLocation')  # 0 = home, 1 = local
	if configLocation == '0':
		configPath = os.path.expandvars('%APPDATA%\TS3Client')
	else:
		configPath = getTS3ClientInstallPath() + "\config"  # Config folder is located inside install path
	if os.path.exists(configPath):
		return configPath
	return None
