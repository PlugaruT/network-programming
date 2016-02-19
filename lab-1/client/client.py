from socket import *

clientSocket = socket()
host = 'localhost'
port = 1233

clientSocket.connect((host, port))
print clientSocket.recv(128)
while True:
    command = raw_input('> ')
    clientSocket.sendall(command)
    data = clientSocket.recv(512)
    print data
    if len(data) == 0: break
clientSocket.close()
