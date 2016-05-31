#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Demonstration how to query the current server and channel data from a running TeamSpeak 3 Client
#

import string
from clientquery import *

HOST = 'localhost'
PORT = 25639

#
# Demonstrate connecting to a local TeamSpeak 3 clientquery
#
def getServerChannelConnectInfo():
	# Create TCP socket and connect to clientquery on localhost:25639
	s = connectTS3Query(HOST, PORT)
	if not s:
		return None

	# Once connected, check if we receive "TS3 Client".
	# If not, this is no TS3 clientquery
	(data, err) = receive(s)
	if err or not data or not string.lower(data[0]).startswith('ts3 client'):
		print 'Not a TS ClientQuery'
		return None

	# Send "currentchannelid" to get the current channel ID
	send(s, 'whoami')
	(data, err) = receive(s)
	if err:
		return None
	#myClientID = int(getParamValue(data[0], 'clid'))  # Unused in this sample
	currentChannelID = int(getParamValue(data[0], 'cid'))

	# Send "serverconnectinfo" to get server IP, port and password
	send(s, 'serverconnectinfo')
	(data, err) = receive(s)
	if err:
		return None
	ip = getParamValue(data[0], 'ip')
	port = int(getParamValue(data[0], 'port'))
	password = getParamValue(data[0], 'password')
	if not ip or not port:
		print 'No IP or port specified'
		return None

	# Send "channelconnectinfo" to get current channel path and password
	send(s, 'channelconnectinfo')
	(data, err) = receive(s)
	if err:
		return None
	path = getParamValue(data[0], 'path').replace('\s', ' ')
	channelPassword = getParamValue(data[0], 'password')
	if not path:
		print 'No channel path specified'
		return None

	# Verify server password
	if password:
		send(s, 'verifyserverpassword password=%s' % password)
		(data, err) = receive(s)
		if err:
			# If a user is ServerAdmin, it is possible he has no password stored in the bookmark as he can connect to the server without password
			# In this case the application should prompt the user for the correct password
			print 'Server password validation failed'
	
	# Verify channel password
	if channelPassword:
		send(s, 'verifychannelpassword cid=%d password=%s' % (currentChannelID, channelPassword))
		(data, err) = receive(s)
		if err:
			# If a user is ServerAdmin or ChannelAdmin, it is possible he has no password stored as he can join the channel without password
			# In this case the application should prompt the user for the correct password
			print 'Channel password validation failed'
	
	# Finally we have the required data available: Current server IP, port, password, current channel path, password
	# Send this data to invite another user and pass it to the startTS3Client function available in the startts3client.py demo.
	return (ip, port, password, path, channelPassword)

def main():
	info = getServerChannelConnectInfo()
	if not info:
		print 'Failed to receive server and channel connect info'
		return
	(ip, port, password, path, channelPassword) = info
	print 'Server: %s:%d, Password: %s' % (ip, port, password)
	print 'Channel: %s, Password: %s' % (path, channelPassword)

if __name__ == '__main__':
	main()
