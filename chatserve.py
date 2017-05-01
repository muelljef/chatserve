from socket import *
import signal
import sys

# Setting a SIG INT or Ctrl + C handler to close the server socket on exit
def signal_handler(signal, frame):
    serverSocket.close()
    print('You pressed Ctrl+C')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Get the port number from the user
try:
    serverPort = int(raw_input('Enter the port number to serve on: '))
except ValueError:
    print 'Invalid port number'
    sys.exit(1)
if serverPort < 1 or serverPort > 65535:
    print 'Invalid port number'
    sys.exit(1)

# Setup the server connection on the given port number
try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
except:
    print 'Failed to bind the port'
    sys.exit(1)
print 'Listening for connections on port ' + str(serverPort) + '\n'

# hard coded server handle
serverHandle = 'ServeO'

# listen for connection
while 1:
    connectionSocket, addr = serverSocket.accept()

    # connection made, loop for conversation
    while 1:
        # read the client message
        peerMessage = connectionSocket.recv(1024)

        # check if client closed the connection, if not print the message to screen
        if not peerMessage:
            "client closed connection"
            break
        print peerMessage

        # get the message from the server
        myMessage = raw_input(serverHandle + '>')
        myMessage = myMessage[:500]

        # check if the server wants to quit the connection
        if myMessage == "\quit":
            print "closing connection"
            break

        # send the message to the client
        myMessage = serverHandle + '>' + myMessage
        connectionSocket.send(myMessage)

    connectionSocket.close()
    print "\nConnection terminated, still serving for chat\n"
