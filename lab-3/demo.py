from Tkinter import *
from Tkinter import Tk
import threading
import select
import random
from socket import *

PORT = 50000

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
canvasWidth = 500
canvasHeight = 400



def gen_hex_colour_code():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for x in range(6)])


color = gen_hex_colour_code()


def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y


def create_msg(x, y, e_x, e_y, color):
    clear_flag = 0
    return '{0}'.format(str(x).zfill(4)) + '{0}'.format(str(y).zfill(4)) + '{0}'.format(str(e_x).zfill(4)) \
           + '{0}'.format(str(e_y).zfill(4)) + str(color)


def add_line(event):
    global lastx, lasty
    canvas.create_line((lastx, lasty, event.x, event.y), fill=str(color), width=2)
    data = create_msg(lastx, lasty, event.x, event.y, color)
    print data
    sock.sendto(data, ('255.255.255.255', PORT))
    lastx, lasty = event.x, event.y


def worker(root, canvas):
    while True:
        result = select.select([s], [], [])
        data = result[0][0].recv(1024)
        canvas.create_line((int(data[0:4]), int(data[4:8]), int(data[8:12]), int(data[12:16])), fill=data[16:23], width=2)



if __name__ == "__main__":
    root = Tk()
    root.title('Shared Whiteboard')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    var = IntVar()
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    canvas.bind("<Button-1>", xy)  # event, mouse-click
    canvas.bind("<B1-Motion>", add_line)  # event, move mouse with a clicked button

    # start another thread, it will read stuff from the socket
    # and update the canvas if needed
    t = threading.Thread(target=worker, args=(root, canvas))
    t.start()
    # drawing the canvas itself
    root.mainloop()
