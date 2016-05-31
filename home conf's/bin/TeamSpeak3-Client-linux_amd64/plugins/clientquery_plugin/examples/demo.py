#
# TeamSpeak 3 ClientQuery example
# Copyright (c) 2010 TeamSpeak Systems GmbH
#
# Demonstration how to monitor clients in the current server
#

import sys, string
from clientquery import *

HOST = 'localhost'
PORT = 25639

STATUS_NOT_TALKING = 0
STATUS_TALKING = 1
STATUS_TALKING_WHILE_DISABLED = 2

clientUIDsGamingWith = [ 'z3vfjIEaWUgvkeD5vikiNhwg1e0=' ]

# Global variables
ownClientID = 0
ownClientUID = ''
currentChannelID = 0
clients = {}

class Client:
	def __init__(self, id, uid, name, channelID):
		self.id = id
		self.uid = uid
		self.name = name
		self.channelID = channelID

	def __str__(self):
		return '%s (%d) %s' % (self.name, self.id, self.uid)

def getDataForCurrentServerTab(s):
	global ownClientID, ownClientUID, currentChannelID, clients
	
	# Clear data
	ownClientID = 0
	ownClientUID = ''
	currentChannelID = 0
	clients = {}

	# Get own clientID and current channel ID
	send(s, 'whoami')
	(data, err) = receive(s)
	if err:
		print 'Error getting whoami info'
		return False
	ownClientID = int(getParamValue(data[0], 'clid'))
	print 'ownClientID:', ownClientID
	currentChannelID = int(getParamValue(data[0], 'cid'))
	print 'currentChannelID:', currentChannelID

	# Get list of clients in current channel
	send(s, 'clientlist -uid')
	(data, err) = receive(s)
	if err:
		print 'Error getting clientlist'
		return False
	cl = data[0].split('|')
	for c in cl:
		clientID = int(getParamValue(c, 'clid'))
		channelID = int(getParamValue(c, 'cid'))
		clients[clientID] = Client(clientID, getParamValue(c, 'client_unique_identifier'), getParamValue(c, 'client_nickname'), channelID)
	for c in clients:
		print clients[c]
		
	# Own client unique id
	ownClientUID = clients[ownClientID].uid
	print 'ownClientUID', ownClientUID

	return True
		
#
# Demonstrate connecting to a local TeamSpeak 3 clientquery
#
def main():
	# Create TCP socket and connect to clientquery on localhost:25639
	s = connectTS3Query(HOST, PORT)
	if not s:
		return

	# Once connected, check if we receive "TS3 Client".
	# If not, this is no TS3 clientquery
	(data, err) = receive(s)
	if err or not data or not string.lower(data[0]).startswith('ts3 client'):
		print 'Not a TS ClientQuery'
		return

	# Get current server tab
	send(s, 'currentschandlerid')
	(data, err) = receive(s)
	if err:
		print 'Error getting currentschandlerid'
		return
	currentScHandlerID = int(getParamValue(data[0], 'schandlerid'))
	print 'currentScHandlerID:', currentScHandlerID
	if not getDataForCurrentServerTab(s):
		print 'Error getting data for current server tab'
		return
	
	# Register for talk status change events
	send(s, 'clientnotifyregister schandlerid=0 event=notifytalkstatuschange')
	(data, err) = receive(s)
	if err:
		print 'Error registering for talk status change events'
		return
		
	# Register for client enter view events
	send(s, 'clientnotifyregister schandlerid=0 event=notifycliententerview')
	(data, err) = receive(s)
	if err:
		print 'Error registering for client enter view events'
		return
		
	# Register for client enter view events
	send(s, 'clientnotifyregister schandlerid=0 event=notifyclientleftview')
	(data, err) = receive(s)
	if err:
		print 'Error registering for client left view events'
		return
	
	# Register for client move events
	send(s, 'clientnotifyregister schandlerid=0 event=notifyclientmoved')
	(data, err) = receive(s)
	if err:
		print 'Error registering for client move events'
		return
		
	# Register for server tab change in the UI
	send(s, 'clientnotifyregister schandlerid=0 event=notifycurrentserverconnectionchanged')
	(data, err) = receive(s)
	if err:
		print 'Error registering for current server tab changed'
		return
	
	try:
		while True:
			(dataLines, err) = receive(s)
			if not dataLines:
				continue
			for data in dataLines:
				if data.startswith('notifytalkstatuschange'):
					scHandlerID = int(getParamValue(data, 'schandlerid'))
					if scHandlerID != currentScHandlerID:
						continue
					status = int(getParamValue(data, 'status'))
					if status == STATUS_TALKING:
						verb = 'starts'
					elif status == STATUS_NOT_TALKING:
						verb = 'stops'
					elif status == STATUS_TALKING_WHILE_DISABLED:
						continue  # Ignore
					cid = int(getParamValue(data, 'clid'))
					if cid == ownClientID:
						# Own client, just display a message and continue
						print 'Own client %s talking.' % verb
					else:
						# Other
						try:
							client = clients[cid]
						except KeyError:
							print 'Error, unknown clientID not in list:', cid
							continue
						# Here we check if the client is in our list of UIDs of clients we see in the game.
						# This info would be fed from the game, for testing purpose I added a UID manually.
						if not client.uid in clientUIDsGamingWith:
							print 'Client %s not in game, ignoring' % client.uid
							continue  # Client not in game, ignore
						print '"%s" %s talking.' % (client.name, verb)
				elif data.startswith('notifyclientmoved'):
					scHandlerID = int(getParamValue(data, 'schandlerid'))
					if scHandlerID != currentScHandlerID:
						continue
					cid = int(getParamValue(data, 'clid'))
					newChannelID = int(getParamValue(data, 'ctid'))
					try:
						client = clients[cid]
					except KeyError:
						print 'Error, unknown clientID not in list:', cid
						continue
					client.channelID = newChannelID  # Adjust channelID in client
					if cid == ownClientID:
						currentChannelID = newChannelID  # Own client moved channel
					elif newChannelID == currentChannelID:
						print '"%s" entered your channel' % client.name
					else:
						print '"%s" left your channel' % client.name
				elif data.startswith('notifycliententerview'):
					scHandlerID = int(getParamValue(data, 'schandlerid'))
					if scHandlerID != currentScHandlerID:
						continue
					newChannelID = int(getParamValue(data, 'ctid'))
					cl = data.split('|')
					for c in cl:
						cid = int(getParamValue(c, 'clid'))
						client = Client(cid, getParamValue(c, 'client_unique_identifier'), getParamValue(c, 'client_nickname'), newChannelID)
						clients[cid] = client
						print '"%s" entered your channel' % client.name
				elif data.startswith('notifyclientleftview'):
					scHandlerID = int(getParamValue(data, 'schandlerid'))
					if scHandlerID != currentScHandlerID:
						continue
					cl = data.split('|')
					for c in cl:
						cid = int(getParamValue(c, 'clid'))
						try:
							name = clients[cid].name
							del clients[cid]  # Remove from clients list
						except KeyError:
							name = 'Unknown'
						print '"%s" left your channel' % name
				elif data.startswith('notifycurrentserverconnectionchanged'):
					currentScHandlerID = int(getParamValue(data, 'schandlerid'))
					print "Tab changed, currentScHandlerID:", currentScHandlerID
					send(s, 'use %d' % currentScHandlerID)  # Let clientquery use new tab
					(data, err) = receive(s)
					print "********", data
					if err:
						print 'Error switching to new server connection'
						return
					if not getDataForCurrentServerTab(s):
						print 'Error getting data for current server tab'
						return
					
	except KeyboardInterrupt:
		send(s, 'quit')
		sys.exit()

if __name__ == '__main__':
	main()
