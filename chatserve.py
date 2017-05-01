#!/usr/bin/python
from socket import *
import signal
import sys

# Setting a SIG INT or Ctrl + C handler to close the server socket on exit

def startUp():
    # Get the port number from the user
    serverPort = 50123

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

    # Set the signal handler for sig int
    def signal_handler(*args):
        serverSocket.close()
        print 'chatserve closing'
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # hard coded server handle
    serverHandle = 'ServeO'
    return serverSocket, serverHandle


def sendMessage(connectionSocket, serverHandle):
    # get the message from the server
    myMessage = raw_input(serverHandle + '>')
    myMessage = myMessage[:500]

    # check if the server wants to quit the connection
    if myMessage == "\quit":
        return False

    # send the message to the client
    myMessage = serverHandle + '>' + myMessage
    connectionSocket.send(myMessage)
    return True


def receiveMessage(connectionSocket):
    # read the client message
    peerMessage = connectionSocket.recv(1024)

    # check if client closed the connection, if not print the message to screen
    if not peerMessage:
        return False
    print peerMessage
    return True


def main(argv):
    serverSocket, serverHandle = startUp()

    # listen for connection
    while 1:
        connectionSocket, addr = serverSocket.accept()

        # connection made, loop for conversation
        while 1:
            if not receiveMessage(connectionSocket):
                print "Client closed connection"
                break

            if not sendMessage(connectionSocket, serverHandle):
                print "Closing connection"
                break

        connectionSocket.close()
        print "\nConnection terminated, still serving for chat\n"

if __name__ == "__main__":
    main(sys.argv[1:])
