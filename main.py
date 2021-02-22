import socket 
import logging
import re
import sys
import getopt
import os
from enum import Enum
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

### TODOS
# TODO Enum for commands 
# TODO varaible mouse movement?
# TODO logging 
# TODO Filter none command messages
# TODO Remove magic numbers for mouse
# TODO Have long and short versions for commands
###

mouse = MouseController()
keyboard = KeyboardController()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

def ParseCommand(message):
    message = message.replace('\r', '')
    if message == 'rm': # Click Right Mouse
        mouse.press(Button.right)
        mouse.release(Button.right)
    elif message == 'hrm': # Hold Right Mouse
        mouse.press(Button.right)
    elif message == 'rrm': # Release Right Mouse
        mouse.release(Button.right)
    elif message == 'lm': # Click Left Mouse
        mouse.press(Button.left)
        mouse.release(Button.left)
    elif message == 'hlm': # Hold Left Mouse
        mouse.press(Button.left)
    elif message == 'rlm': # Release Left Mouse
        mouse.release(Button.left)
    elif message == 'mup':
        mouse.move(0,-60)
    elif message == 'mdown':
        mouse.move(0,60)
    elif message == 'mleft':
        mouse.move(-60, 0)
    elif message == 'mright':
        mouse.move(60,0)
    elif message == 'halt': # Hold Alt
        keyboard.press(Key.alt)
    elif message == 'ralt': # Release Alt
        keyboard.release(Key.alt)
    elif message == "Z": # Press Z
        keyboard.press('z')
        keyboard.release('z')
    elif message == 'w': # Press W
        keyboard.press('w')
        keyboard.release('w')
    elif message == 's': # Press S
        keyboard.press('s')
        keyboard.release('s')
    elif message == 'a': # Press A
        keyboard.press('a')
        keyboard.release('a')
    elif message == 'd': # Press D
        keyboard.press('d')
        keyboard.release('d')
    elif message == 'hw': # Hold W
        keyboard.press('w')
    elif message == 'ha': # Hold A
        keyboard.press('a')
    elif message == 'hs': # Hold S
        keyboard.press('s')
    elif message == 'hd': # Hold D
        keyboard.press('d')
    elif message == 'rw': # Release W
        keyboard.release('w')
    elif message == 'ra': # Release A
        keyboard.release('a')
    elif message == 'rs': # Release S
        keyboard.release('s')
    elif message == 'rd': # Release D
        keyboard.release('d')
    elif message == 'ctrl': # Press Ctrl
        keyboard.press(Key.ctrl)
        keyboard.release(Key.ctrl)
    elif message == 'f':  # Press F (to pay respect?)
        keyboard.press('f')
        keyboard.release('f')
    elif message == 'clock': # Press Caps Lock
        keyboard.press(Key.caps_lock)
        keyboard.release(Key.caps_lock)
    elif message == 't': # Press T
        keyboard.press('t')
        keyboard.release('t') 
    elif message == 'j': # Press J
        keyboard.press('j')
        keyboard.release('j')
    elif message == 'e': # Press E
        keyboard.press('e')
        keyboard.release('e')
    elif message == 'tab': # Press Tab
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif message == 'r': # Press R
        keyboard.press('r')
        keyboard.release('r')
    elif message == 'space': # Press Space
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif message == 'he': # Hold E
        keyboard.press('e')
    elif message == 're': # Release E
        keyboard.release('re')
    elif message == 'q': # Press Q
        keyboard.press('q')
        keyboard.release('q')
    elif message == 'esc': # Press Escape
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif message == 'f5': # Press F5
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif message == 'up': # Press Up
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif message == 'down': # Press Down
        keyboard.press(Key.down)
        keyboard.press(Key.down)
    elif message == 'left': # Press Left
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif message == 'right': # Press Right
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif message == 'hshift': # Hold Shift
        keyboard.press(Key.shift_l)
    elif message == 'rshift': # Release Shift
        keyboard.release(Key.shift_l)
    elif message == 'enter': # Press Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif message == 'moo': #Test Command
        print('Said The Blue Cow')
    else:
        print('Not A Recognized command: ' + message)

def main(argv):
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'InputBoi'
    token = os.environ.get('twitch_token')
    channel = ''

    try:
        opts, args = getopt.getopt(argv, "hc:",["channel="])
    except getopt.GetoptError:
        print('main.py -c <channel>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -c <channel>')
            sys.exit()
        elif opt in ('-c', '--channel'):
            channel = '#' + arg

    print('Connection to channel ' + channel)
    sock = socket.socket()
    sock.connect((server, port))
    print('Connected!')

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    try:
        print('Beginning command parsing...')
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                fmtre = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp)
                if fmtre is not None:
                    username, channel, message = fmtre.groups()
                    # print(f"Channel: {channel} \nUsername: {username} \nMessage: {message}")
                    ParseCommand(message)
    except KeyboardInterrupt:
        sock.close()
        print('Socket Closed')

if __name__ == "__main__":
    main(sys.argv[1:])



