# Import socket module
# Import sys to retrieve the arguments
from socket import *
import sys

# Checking to see if we do have four arguments
if (len(sys.argv) != 4):
    print("Wrong number of arguments.")
    print("Use: webclient.py <server_host> <server_port> <filename>")
    sys.exit()

# Preparing the socket
serverHost, serverPort, filename = sys.argv[1:]
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverHost, int(serverPort)))
except: # In case the server is not available
    print("Sorry, the server is currently offline or busy.")
    clientSocket.close()
    sys.exit()
print("Connection OK.")

# Sending the HTTP request
httpRequest = "GET /" + filename + " HTTP/1.1\r\n\r\n"
clientSocket.send(httpRequest.encode())
print("Request message sent.")

# Recieving the response
print("Server HTTP Response:\r\n")

# This loop is necessary because we don't know if the entire message will be
# recieved at the same recv() call. If there is a timeout and no new data has
# arrived, we have the entire response.
data = ""
while True:
    clientSocket.settimeout(5)
    newData = clientSocket.recv(1024).decode()
    data += newData
    if (len(newData) == 0):
        break
print(data)

# Closing socket and ending the program
print("Closing socket . . .")
clientSocket.close()
