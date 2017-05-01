#!/usr/bin/python
from socket import *
import signal
import sys

'''
    Sources used to generate code for 
    // The following provided code sample for accessing command line arguments and calling main() method
    https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    
    // The following provided the code sample for registering the signal handler
    http://stackoverflow.com/questions/12371361/using-variables-in-signal-handler-require-global

    // The following was used to setup the socket server
    http://www.binarytides.com/python-socket-programming-tutorial/
    
    // Referenced in the code as well, this solution made the socket available immediately after the program is closed
    http://stackoverflow.com/questions/27360218/how-to-close-socket-connection-on-ctrl-c-in-a-python-programm
'''


'''
    The main control for the program
'''
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



'''
    startUp(): start the server by creating a socket and listening for connections from
        any host on the specified port. Also sets the sig int handle to ensure socket is closed
        when exiting
    success: returns a tuple of a server socket object and a string handle
    failure: prints error to screen and exits the program
'''
def startUp():
    serverPort = getPortNumber()

    # Setup the server connection on the given port number
    try:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # the following link provided the solution to make the socket available immediately after closing the program
        # http://stackoverflow.com/questions/27360218/how-to-close-socket-connection-on-ctrl-c-in-a-python-programme
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
        print '\nchatserve closing'
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # hard coded server handle
    serverHandle = 'ServeO'
    return serverSocket, serverHandle


'''
    getPortNumber(): Gets the port number from the command line arguments and converts it to an integer
    success: returns int serverPort
    failure: prints error to screen and exits the program
'''
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


'''
    sendMessage(connectionSocket, serverHandle): send a message to the chatclient program
    returns False when user has indicating they want to close connection
    returns True when message has successfully been sent
'''
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


'''
    receiveMessage(connectionSocket): receives a message from the chatclient program
    returns False when chatclient has closed connection
    returns True when message has successfully been received
'''
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
