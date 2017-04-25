#!/usr/bin/python
from socket import *

serverName = 'localhost'
serverPort = 50517

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

serverHandle = 'ServeO'

while 1:
    connectionSocket, addr = serverSocket.accept()

    while 1:
        peerMessage = connectionSocket.recv(1024)
        if not peerMessage:
            break
        print peerMessage

        myMessage = raw_input(serverHandle + '>')
        myMessage = serverHandle + '>' + myMessage
        connectionSocket.send(myMessage)

    print "\nConnection terminated, still serving for chat\n"

connectionSocket.close()