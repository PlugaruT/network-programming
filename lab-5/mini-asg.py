import sys, time
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
data = '2#Main\x00tudor\x00some text\x00'
s.sendto(data, ('<broadcast>', 8167))
