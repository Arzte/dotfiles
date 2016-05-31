#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Common clientquery functions
#

import sys, socket

#
# Get value by key from "key=value" string
#
def getParamValue(data, key):
	datas = data.split()
	for data in datas:
		s = data.split('=', 1)
		if s[0] == key:
			return s[1]
	return None

#
# Build "key=value" string from list of tuples
#
def buildParam(datas):
	param = ''
	for data in datas:
		if not data:
			break
		param += '%s=%s' % (data[0], data[1])
	return param

#
# Check received data for error message
# Return None if no error occured. Otherwise return a tuple (errorID, errorMessage).
#
def checkError(data):
	if not data[0].startswith('error '):
		return None
	e = data[0].split()
	id = int(getParamValue(e[1], 'id'))
	if id == 0:  # ERROR_ok == 0
		return None
	msg = getParamValue(e[2], 'msg').replace('\s', ' ')
	print 'Error: %s (%d)' % (msg, id)
	return (id, msg)

#
# Receive data from socket and check received lines if an error occured.
# Return a tuple (list of messages, (errorID, errorMessage))
# If no error occured, return (list of messages, None)
#
def receive(s):
	lines = []
	data = ''
	while True:
		try:
			d = s.recv(1024)
		except socket.error, err:
			if type(err) != socket.timeout:
				print 'Error receiving from server: %s' % err
				sys.exit(0)
			break
		if not d:
			continue
		data += d
		while '\n\r' in data:
			datas = data.split('\n\r', 1)
			lines.append(datas[0])
			print '<<', datas[0]
			data = datas[1]
		if len(lines) > 0:
			last = lines[len(lines)-1]
			if last.startswith('error '):
				break  # Avoid waiting for timeout as the last line usually is an error message
			elif len(lines) == 3 and last.startswith('selected schandlerid=1'):
				break  # Avoid waiting for timeout on connect message
	if len(lines) == 0:
		return (None, None)
	return (lines, checkError(lines))

#
# Send data to socket
#
def send(s, data):
	print '>>', data
	s.send(data + '\r\n')

#
# Demonstrate connecting to a local TeamSpeak 3 clientquery
#
def connectTS3Query(host, port):
	# Create TCP socket and connect to clientquery on localhost:25639
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, port))
	except socket.error:
		print 'Failed to connect to %s:%d' % (host, port)
		return None
	s.settimeout(0.5)
	return s
