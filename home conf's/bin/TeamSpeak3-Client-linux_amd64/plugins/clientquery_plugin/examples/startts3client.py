#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Demonstration how to start the TeamSpeak 3 client and connect to a specified server and channel
#

import connectinfo, ts3paths, subprocess

#
# Start TeamSpeak 3 client if found and connect to the specified server and channel.
#
def startTS3Client(ip, port, serverPassword, channelPath, channelPassword, nickname):
	binaryPath = ts3paths.getTS3ClientBinaryPath()
	if not binaryPath:
		print 'TS3 Client binary not found'
		return
	# ts3server://localhost?port=9987&nickname=Test User&password=secret&channel=test&channelpassword=testpw
	ts3ServerLink = 'ts3server://%s?port=%d&nickname=%s&password=%s&channel=%s&channelpassword=%s' % (ip, port, nickname, serverPassword, channelPath, channelPassword)
	cmd = '""%s" "%s""' % (binaryPath, ts3ServerLink)  # Windows wants each path and parameter quoted and the whole command double-quoted
	subprocess.Popen(cmd, shell=True)

#
# Demonstrate how to start a TeamSpeak 3 client and connect to the specified server and channel
#	
def mainDummy():
	# The information for the server and channel parameters can be obtained with the clientQuery, see the simple.py demo
	startTS3Client('localhost', 9987, 'testthewest', 'test/subtest', '', 'Test Dude')

def main():
	# A real test: Connect to same channel and server as the first servertab in the TeamSpeak 3 client
	info = connectinfo.getServerChannelConnectInfo()
	if not info:
		print 'Failed to receive server and channel connect info'
		return
	(ip, port, password, path, channelPassword) = info
	print 'Server: %s:%d, Password: %s' % (ip, port, password)
	print 'Channel: %s, Password: %s' % (path, channelPassword)
	startTS3Client(ip, port, password, path, channelPassword, 'Test Dude')
	
if __name__ == '__main__':
	#mainDummy()
	main()
