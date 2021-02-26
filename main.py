import socket 
import logging
import re
import sys
import getopt
import os
import time
from enum import Enum
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController, Listener

### NOTES
# Disable alt-tab so you can't leave the game
# Can I lock the game?


### TODOS
# TODO Replace ELIF with tuples and better commands 
# TODO mleft0*1A4 broke it 
# TODO mouse to lmb and rmb
# TODO can something be down about the mouse snap?
# TODO F5 is broken from regex
# TODO Limit mouse move size
# TODO Mouse key is broken?
# TODO Better logging, breaking and not knowing 
# TODO Have long and short versions for commands
###

MOUSE_STEP=100
sock = socket.socket()
mouse = MouseController()
keyboard = KeyboardController()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def click_right():
    mouse.press(Button.right)
    time.sleep(0.3)
    mouse.release(Button.right)

def click_left():
    mouse.press(Button.left)
    time.sleep(0.3)
    mouse.release(Button.left)

def mouse_up(y):
    mouse.position = (1,1)
    if value != '':
        mouse.move(0,-int(value))
    else:
        mouse.move(0,-MOUSE_STEP)

def mouse_down(y):
    mouse.position = (1,1)
    if value != '':
        mouse.move(0,int(value))
    else:
        mouse.move(0,MOUSE_STEP)

def mouse_left(x):
    mouse.position = (1,1)
    if value != '':
        mouse.move(-int(value), 0)
    else:
        mouse.move(-MOUSE_STEP, 0)

def mouse_right(x):
    mouse.position = (1,1)
    if value != '':
        mouse.move(int(value), 0)
    else:    
        mouse.move(MOUSE_STEP,0)

def reset_buttons():
    mouse.release(Mouse.right)
    mouse.release(Mouse.left)
    keyboard.release('w')
    keyboard.release('s')
    keyboard.release('a')
    keyboard.release('d')
    keyboard.release('e')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.alt)

def on_move(x,y):
    print("print('Pointer moved to {0}".format((x,y)))

commands = [
    # (command, function)
    ('rmb', click_right),
    ('hrmb', lambda: mouse.press(Button.right)),
    ('rrmb', lambda: mouse.release(Button.right)),
    ('lmb', click_left),
    ('hlmb', lambda: mouse.press(Button.left)),
    ('rlmb', lambda: mouse.release(Button.left)),
    ('mup', mouse_up),
    ('mdown', mouse_down),
    ('mleft', mouse_left),
    ('mright', mouse_right),
    ('halt', lambda: keyboard.press(Key.alt)),
    ('ralt', lambda: keyboard.release(Key.alt)),
    ('z',  lambda: press_key('z')),
    ('w', lambda: press_key('w')),
    ('s', lambda: press_key('s')),
    ('a', lambda: press_key('a')),
    ('d', lambda: press_key('d')),
    ('hw', lambda: keyboard.press('w')),
    ('hs', lambda: keyboard.press('a')),
    ('ha', lambda: keyboard.press('s')),
    ('hd', lambda: keyboard.press('d')),
    ('rw', lambda: keyboard.release('w')),
    ('rs', lambda: keyboard.release('a')),
    ('ra', lambda: keyboard.release('s')),
    ('rd', lambda: keyboard.release('d')),
    ('ctrl', lambda: press_key(Key.ctrl)),
    ('f', lambda: press_key('f')),
    ('clock', lambda: press_key(Key.caps_lock)),
    ('t', lambda: press_key('t')),
    ('j', lambda: press_key('j')),
    ('e', lambda: press_key('e')),
    ('tab', lambda: press_key(Key.tab)),
    ('r', lambda: press_key('r')),
    ('l', lambda: press_key('l')),
    ('m', lambda: press_key('m')),
    ('space', lambda: press_key(Key.space)),
    ('he', lambda: keyboard.press('e')),
    ('re', lambda: keyboard.release('e')),
    ('q', lambda: press_key('q')),
    ('esc', lambda: press_key(Key.esc)),
    ('f5', lambda: press_key(Key.f5)),
    ('up', lambda: press_key(Key.up)),
    ('down', lambda: press_key(Key.down)),
    ('left', lambda: press_key(Key.left)),
    ('right', lambda: press_key(Key.right)),
    ('hshift', lambda: keyboard.press(Key.shift_l)),
    ('rshift', lambda: keyboard.release(Key.shift_l)),
    ('enter', lambda: press_key(Key.enter)),
    ('reset_buttons', reset_buttons),
    ('moo', lambda: print('Said The Blue Cow')),
]

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
    sock.connect((server, port))
    print('Connected!')
    logging.debug('Connection Started')

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
                    message = message.replace('\r', '')
                    # print(f"Channel: {channel} \nUsername: {username} \nMessage: {message}")
                    msg = re.search('([a-zA-Z]+)[ ]?([0-9]*)',message)
                    if msg != None:
                        command, value = msg.groups()
                        for c in commands:
                            if command == c[0]:
                                c[1]() if value != None else c[1](value) 
                                logging.debug("{}:{}:{}:{}".format(channel,username,command,value))
                                break
                            

    except KeyboardInterrupt:
        sock.close()

        print('Socket Closed')
    except ConnectionError:
        sock.close()
        print('Connection Error')
    except Exception:
        logging.error('Fuck: ' + Exception.msg)

if __name__ == "__main__":
    main(sys.argv[1:])



