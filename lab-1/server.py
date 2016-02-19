from socket import *
from time import gmtime, strftime
from thread import *


serverSocket = socket()
host = 'localhost'
port = 1233
message = 'Hello Master'

serverSocket.bind((host, port))

# queue up to 5 requests
serverSocket.listen(5)

def client_thread(connection):
    f = open('arn.jpg', 'rb')
    l = f.read(1024)
    while True:
        data = connection.recv(512)
        if not data: break
        tokens = data.split(' ',1)
        command = tokens[0]
        if command == 'time':
            reply = strftime("%H:%M:%S", gmtime())
        elif command == 'date':
            reply = strftime("%Y-%m-%d", gmtime())
        elif command == 'add':
            numbers = tokens[1].split('+')
            reply = str(int(numbers[0]) + int(numbers[1]))
        elif command == 'mul':
            numbers = tokens[1].split('*')
            reply = str(int(numbers[0]) * int(numbers[1]))
        elif command == 'div':
            numbers = tokens[1].split('/')
            reply = str(int(numbers[0]) / int(numbers[1]))
        elif command.find('?') > 0:
            reply = '42'
        elif command == 'rev':
            reply = tokens[1][::-1]
        elif command == 'pic':
            while True:
                connection.send(l)
                l = f.read(1024)
                break
        elif command == 'hastalavista':
            connection.sendall("I'll be back!")
            connection.close()
            serverSocket.shutdown(SHUT_RDWR)
            serverSocket.close()
            break
        elif command == 'close':
            connection.close()
            break
        else:
            reply = 'Can you elaborate on that?'

        if len(reply) > 0:
            connection.sendall(reply)


while True:
    # establish connection
    clientSocket, addr = serverSocket.accept()
    print("Got a connection from %s" % str(addr))
    start_new_thread(client_thread,(clientSocket,))
    clientSocket.sendall(message + str(addr).split(',')[1].replace(')', ''))

clientSocket.close()
serverSocket.close()
