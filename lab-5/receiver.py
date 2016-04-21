import select, socket 

port = 8167 
bufferSize = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(0)
sock.bind(('', 0))

while True:
    r, w, x = select.select([sock],[],[])
    msg = r[0][0].recvfrom(bufferSize) 
    print msg