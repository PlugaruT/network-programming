import sys 
import time
from socket import *

PORT = 8167

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.setblocking(0)


def public_msg(user_name, channel, text):
    return '2#{channel}\x00{user_name}\x00{string}'.format(channel=channel, user_name=user_name, string=text) 


def private_msg(from_name, to_name, text):
    return 'J2{from_name}\x00{to_name}\x00{string}\x00'.format(from_name=from_name, to_name=to_name, string=text)


def private_personal_msg(from_name, to_name, msg):
    return '6{from_name}\x00{to_name}\x00{message}\x00'.format(from_name=from_name, to_name=to_name, message=msg)


def change_name(old_name, new_name):
    return '3{old_name}\x00{new_name}\x000'.format(old_name=old_name, new_name=new_name)


def change_topic(topic_name):
    return 'B{name}'.format(name=topic_name)


def join_channel(user_name, ch_name):
    return 'K{user_name}\x00#{ch_name}\x00{user_name}\x001'.format(user_name=user_name, ch_name=ch_name)


def leave_channel(user_name, ch_name):
    return '5{user_name}\x00#{ch_name}\x000'.format(user_name=user_name, ch_name=ch_name)


def change_status(user_name, status):
    switcher = {
        'available': '  '.format(user_name=user_name),
        'dnd': 'D{user_name}\x0010'.format(user_name=user_name),
        'away': 'D{user_name}\x0020'.format(user_name=user_name),
        'offline': 'D{user_name}\x0030'.format(user_name=user_name)
    }
    return switcher.get(status, 'D' + user_name + '\x0000')


# s.sendto(change_status('tudor', 'dnd'), ('<broadcast>', PORT))
s.sendto(private_msg('tudor', 'tudor', 'aaaaaa'), ('<broadcast>', PORT))
# s.sendto(public_msg('bardosik', 'Main', 'llllll'), ('<broadcast>', PORT))
# s.sendto(change_topic('New Topic'), ('<broadcast>', PORT))
