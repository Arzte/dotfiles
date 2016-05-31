Interacting with the TS3 Client from other Applications or Scripts
==================================================================

How can the TS3 Client be used from the outside?
++++++++++++++++++++++++++++++++++++++++++++++++

There are two main ways to interact with the TS3 Client:
- When the Client is not running, you can get information from configuration
  files, and run the Client passing it parameters to e.g. make it connect to
  certain servers. The "startts3client.py" and "connectbookmark.py" example
  python scripts show how this works, see below for a more detailed description
  of each example.
- When the Client is running it listens to a tcp socket providing a service we
  call ClientQuery. This can both be used to fire off commands (e.g. switch
  to a certain channel), or to query information (e.g. what is my nickname)
  or to register for certain events (e.g. talkStatusChange events are fired
  whenever somebody starts or stop talking). The "connectinfo.py" and "demo.py"
  examples show you ways this can be used.

Some more information about ClientQuery
+++++++++++++++++++++++++++++++++++++++

The ClientQuery plugin offers a telnet interface on localhost:25639 to remote
control the TeamSpeak client. This allows an application to integrate with the
TeamSpeak client by connecting to the ClientQuery port.

Here is an example where we connect to the ClientQuery port via telnet:
$ telnet localhost 25639
> TS3 Client
> Welcome to the TeamSpeak 3 ClientQuery interface, type "help" for a list of
> commands and "help <command>" for information on a specific command.
> selected schandlerid=1

As also noted in the output, the "help" command can be used to learn which
commands are available, and "help command" will tell you more information about
the specified command. This information is also available in text file form in
the "plugins/clientquery_plugin" folder in your TS3 Client Installation.

In addition to actively sending commands and waiting for the reply, one can
register for a set of events if the integrating application needs to be notified
by certain actions in the client. To reduce overhead, no notifications are sent
by default. See 'help clientnotifyregister' on how to register for specific
notifications.


What do the Examples do that are provided?
++++++++++++++++++++++++++++++++++++++++++

The Python scripts in the examples directory provide some examples on how to
interact with the TS3 Client from your scripts or applications.

Python verson 2.7 is used for these example scripts.

connectinfo.py
--------------
Checks if I am running a TS3 client, then proceeds to retrieve the server IP,
server password, channel name and channel password I am currently in.
This info could be used to invite somebody to join me on teamspeak.

startts3client.py
-----------------
Starts a TeamSpeak client and connects to the specified server and channel.
This shows how, uppon receiving the data found in "connectinfo.py", a differnt
client would start a TS3 Client and connect to the specified server and channel.

connectbookmark.py
------------------
Lists the servers I have bookmarked, and shows how to start up TeamSpeak and
connect to one of these bookmarks. This could be used to present a user that has
TeamSpeak installed but currently not running a choice of his own favorite servers
to join from within a game.

demo.py
-------
More advanced demonstration on how to monitor users on multiple server tabs.
Shows when users join or leave your channel and start or stop talking.
Demonstrates how to filter clients by their unique id to synchronize with
in-game users.

Other
-----
The two files "clientquery.py" and "ts3paths.py" are not stand alone examples but
rather contain helper functions that the above examples use.
