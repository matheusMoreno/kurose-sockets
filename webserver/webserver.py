# Import socket module
# Import sys to terminate the program
from socket import *
import sys

# Preparing the socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12345 # Arbitrary port number
serverSocket.bind(('',serverPort)) # Binding the port to the socket
serverSocket.listen(1) # Waiting for a request
print("Ready to serve . . .")

while True:
    connectionSocket, addr = serverSocket.accept() # Accepting request
    print("Request accepted from (address, port) tuple: %s" % (addr,))

    try:
        # Recieve message and check file name
        message = connectionSocket.recv(2048).decode()
        filename = message.split()[1]
        f = open(filename[1:], 'r')
        outputdata = f.read()

        print("File found.")
        # Returns header line informing that the file was found
        headerLine = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(headerLine.encode())
        connectionSocket.send("\r\n".encode())

        # Sends the file
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Terminates the conection
        print("File sent.")
        connectionSocket.close()

    except IOError:
        print("Warning: file not found.")

        # Returns the error header to the browser
        errHeader = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(errHeader.encode())
        connectionSocket.send("\r\n".encode())

        # Opens and sends the error page to the browser
        ferr = open("notfound.html", 'r')
        outputerr = ferr.read()

        for i in range(0, len(outputerr)):
            connectionSocket.send(outputerr[i].encode())
        connectionSocket.send("\r\n".encode())

        # Terminates the connection
        print("Error message sent.")
        connectionSocket.close()

    # Closes the application
    serverSocket.close()
    sys.exit()
