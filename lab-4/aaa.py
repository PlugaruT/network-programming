import socket
 
#create an INET, raw socket
# s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
# receive a packet
while True:
  print s.recvfrom(65565)