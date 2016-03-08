import socket

mysock = socket.socket()
mysock.connect(('google.com', 80))
request = 'GET / HTTP/1.1\r\n\r\n'
mysock.send(request)
response = mysock.recv(300000)
# print response
part = response.split('\r\n\r\n')
print part[0]
open('file.txt', 'wb').write(part[1])
mysock.close()
