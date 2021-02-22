import socket 
import logging
import re
import sys
import getopt
import os
from enum import Enum
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController, Listener

### TODOS
# TODO Fix the damn mouse input
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

def on_move(x,y):
    print("print('Pointer moved to {0}".format((x,y)))


def ParseCommand(message):
    MOUSE_STEP=100
    message = message.replace('\r', '')
    commands = re.search('([a-zA-Z]*)([0-9]*)',message)
    if commands is None:
        return
    command, value = commands.groups()
    print('Parsing: ' + command)
    if command == 'rm': # Click Right Mouse
        mouse.press(Button.right)
        mouse.release(Button.right)
    elif command == 'hrm': # Hold Right Mouse
        mouse.press(Button.right)
    elif command == 'rrm': # Release Right Mouse
        mouse.release(Button.right)
    elif command == 'lm': # Click Left Mouse
        mouse.press(Button.left)
        mouse.release(Button.left)
    elif command == 'hlm': # Hold Left Mouse
        mouse.press(Button.left)
    elif command == 'rlm': # Release Left Mouse
        mouse.release(Button.left)
    elif command == 'mup':
        mouse.position = (1,1)
        if value != '':
            mouse.move(0,-int(value))
        else:
            mouse.move(0,-MOUSE_STEP)
    elif command == 'mdown':
        mouse.position = (1,1)
        if value != '':
            mouse.move(0,int(value))
        else:
            mouse.move(0,MOUSE_STEP)
    elif command == 'mleft':
        mouse.position = (1,1)
        if value != '':
            mouse.move(-int(value), 0)
        else:
            mouse.move(-MOUSE_STEP, 0)
    elif command == 'mright':
        mouse.position = (1,1)
        if value != '':
            mouse.move(int(value), 0)
        else:    
            mouse.move(MOUSE_STEP,0)
    elif command == 'reset_mouse':
        mouse.position = (1,1)
    elif command == 'halt': # Hold Alt
        keyboard.press(Key.alt)
    elif command == 'ralt': # Release Alt
        keyboard.release(Key.alt)
    elif command == "Z": # Press Z
        keyboard.press('z')
        keyboard.release('z')
    elif command == 'w': # Press W
        keyboard.press('w')
        keyboard.release('w')
    elif command == 's': # Press S
        keyboard.press('s')
        keyboard.release('s')
    elif command == 'a': # Press A
        keyboard.press('a')
        keyboard.release('a')
    elif command == 'd': # Press D
        keyboard.press('d')
        keyboard.release('d')
    elif command == 'hw': # Hold W
        keyboard.press('w')
    elif command == 'ha': # Hold A
        keyboard.press('a')
    elif command == 'hs': # Hold S
        keyboard.press('s')
    elif command == 'hd': # Hold D
        keyboard.press('d')
    elif command == 'rw': # Release W
        keyboard.release('w')
    elif command == 'ra': # Release A
        keyboard.release('a')
    elif command == 'rs': # Release S
        keyboard.release('s')
    elif command == 'rd': # Release D
        keyboard.release('d')
    elif command == 'ctrl': # Press Ctrl
        keyboard.press(Key.ctrl)
        keyboard.release(Key.ctrl)
    elif command == 'f':  # Press F (to pay respect?)
        keyboard.press('f')
        keyboard.release('f')
    elif command == 'clock': # Press Caps Lock
        keyboard.press(Key.caps_lock)
        keyboard.release(Key.caps_lock)
    elif command == 't': # Press T
        keyboard.press('t')
        keyboard.release('t') 
    elif command == 'j': # Press J
        keyboard.press('j')
        keyboard.release('j')
    elif command == 'e': # Press E
        keyboard.press('e')
        keyboard.release('e')
    elif command == 'tab': # Press Tab
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif command == 'r': # Press R
        keyboard.press('r')
        keyboard.release('r')
    elif command == 'space': # Press Space
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif command == 'he': # Hold E
        keyboard.press('e')
    elif command == 're': # Release E
        keyboard.release('re')
    elif command == 'q': # Press Q
        keyboard.press('q')
        keyboard.release('q')
    elif command == 'esc': # Press Escape
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif command == 'f5': # Press F5
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif command == 'up': # Press Up
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif command == 'down': # Press Down
        keyboard.press(Key.down)
        keyboard.press(Key.down)
    elif command == 'left': # Press Left
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif command == 'right': # Press Right
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif command == 'hshift': # Hold Shift
        keyboard.press(Key.shift_l)
    elif command == 'rshift': # Release Shift
        keyboard.release(Key.shift_l)
    elif command == 'enter': # Press Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif command == 'moo': #Test Command
        print('Said The Blue Cow')
    else:
        print('Not A Recognized command: ' + command)

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

    listener = Listener(on_move=on_move)
    # listener.start()

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
    except ConnectionError:
        sock.close()
        print('Connection Error')

if __name__ == "__main__":
    main(sys.argv[1:])



