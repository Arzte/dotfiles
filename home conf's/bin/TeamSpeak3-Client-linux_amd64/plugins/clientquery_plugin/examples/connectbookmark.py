#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Demonstration how to read the TeamSpeak 3 client bookmark file and connect to the first bookmark UID
#

import ts3paths, os, subprocess

#
# Get list of bookmarks from bookmarks.ini in TeamSpeak 3 client config folder
#	
def getTS3Bookmarks():
	# Get paths to bookmarks.ini
	configPath = ts3paths.getTS3ClientConfigPath()
	bookmarksIni = configPath + r'\bookmarks.ini'
	if not os.path.exists(bookmarksIni):
		print 'TeamSpeak 3 client bookmarks file not found'
		return
	# Read bookmarks.ini
	f = open(bookmarksIni, 'r')
	s = f.read()
	f.close()
	lines = s.split('\n')
	# Read bookmark names and uuids
	names = {}
	uuids = {}
	for l in lines:
		try:
			n = int(l.split('\\')[0])
		except ValueError:
			continue
		if l.startswith('%d\Name' % n):
			names[n] = l.split('=')[1]
		elif l.startswith('%d\Uuid' % n):
			uuids[n] = l.split('=')[1]
	# Merge names and uuids. Reason for two-step process is that it's not guaranteed that <n>\Name comes before <n>\Uuid in bookmarks.ini
	bookmarks = {}
	for n in names:
		bookmarks[n] = (names[n], uuids[n])
	return bookmarks

#
# Start TeamSpeak 3 client if found and connect to the specified bookmark uuid.
#
def startTS3Client(uuid):
	binaryPath = ts3paths.getTS3ClientBinaryPath()
	# TEST STUFF
	binaryPath = 'M:/projects/ts3/teamspeakLagos/client.exe'
	# /TEST STUFF
	if not binaryPath:
		print 'TS3 Client binary not found'
		return
	cmd = '""%s" "connectbookmark=%s""' % (binaryPath, uuid)  # Windows wants each path and parameter quoted and the whole command double-quoted
	print cmd
	subprocess.Popen(cmd, shell=True)
	
def main():
	bookmarks = getTS3Bookmarks()
	for n in bookmarks:
		print '%d\t%s' % (n, bookmarks[n][0])
	print
	s = raw_input('Select bookmark number to connect to: ')
	try:
		n = int(s)
	except ValueError:
		print 'Not a number'
		return
	try:
		uuid = bookmarks[n][1]
	except KeyError:
		print 'Unknown bookmark number:', n
		return
	print 'Connecting to bookmark uuid: %s' % uuid
	startTS3Client(uuid)
	
if __name__ == '__main__':
	main()
