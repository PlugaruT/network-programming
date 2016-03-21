from Tkinter import *
from Tkinter import Tk
import time
import threading
import select
import random
from socket import *

PORT = 1234

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 0))
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.setblocking(0)


s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.bind(('', PORT))
s.setblocking(0)

lastx, lasty = 0, 0
canvasWidth = 300
canvasHeight = 300

def doFoo(*args):
    print "Virtual event was generated"

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):
    global lastx, lasty
    canvas.create_line((lastx, lasty, event.x, event.y))
    sock.sendto(str(lastx) + ' ' + str(lasty) + ' ' + str(event.x) + ' ' + str(event.y), ('<broadcast>', PORT))
    lastx, lasty = event.x, event.y

def dot(canvas, x, y):
	canvas.create_oval(x, y, x+1, y+1)


def worker(root, canvas):
	while True:
		result = select.select([s],[],[])
		msg = result[0][0].recv(1024) 
		coordinates = msg.split(' ')
		canvas.create_line((int(coordinates[0]), int(coordinates[1]), int(coordinates[2]), int(coordinates[3])))


if __name__ == "__main__":
	root = Tk()
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	root.bind("<<Foo>>",doFoo) #event, custom (not tied to the mouse/keyboard)

	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.grid(column=0, row=0, sticky=(N, W, E, S))
	canvas.bind("<Button-1>", xy) #event, mouse-click
	canvas.bind("<B1-Motion>", addLine) #event, move mouse with a clicked button

	#start another thread, it will read stuff from the socket
	#and update the canvas if needed
	t = threading.Thread(target=worker, args=(root, canvas) )
	t.start()
	
	#drawing the canvas itself
	root.mainloop()