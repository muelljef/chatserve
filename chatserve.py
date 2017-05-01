#!/usr/bin/python
from socket import *
import signal
import sys



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



def startUp():
    serverPort = getPortNumber()

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

    # Setting a SIG INT or Ctrl + C handler to close the server socket on exit
    def signal_handler(*args):
        serverSocket.close()
        print 'chatserve closing'
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # hard coded server handle
    serverHandle = 'ServeO'
    return serverSocket, serverHandle



def getPortNumber():
    # Get the port number
    if len(sys.argv) < 2:
        print 'usage: chatserve <port #>'
        sys.exit(1)

    try:
        serverPort = int(sys.argv[1])
    except ValueError:
        print 'Invalid port number ' + sys.argv[1]
        sys.exit(1)

    if serverPort < 1 or serverPort > 65535:
        print 'Invalid port number ' + str(serverPort)
        sys.exit(1)

    return serverPort



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



if __name__ == "__main__":
    main(sys.argv[1:])
