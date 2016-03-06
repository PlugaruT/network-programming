from socket import *

clientSocket = socket()
host = 'localhost'
port = 1234

clientSocket.connect((host, port))
print clientSocket.recv(128)
while True:
    command = raw_input('> ')
    clientSocket.sendall(command)
    if command == 'pic':
    	data_to_receive = clientSocket.recv(20)
    	f = open('new_arn.jpg', 'wb')
    	data_to_receive = int(data_to_receive)
        response = clientSocket.recv(data_to_receive)
        f.write(response)
        data = 'Image received'
        f.close()
    else:
    	data = clientSocket.recv(512)
    print data
    if len(data) == 0: break
clientSocket.close()
