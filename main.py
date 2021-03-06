import socket 
import logging
import re
import sys
import getopt
import os
import time
from queue import Queue
from threading import Thread
from enum import Enum
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KListener
from pynput.mouse import Button, Controller as MouseController, Listener as MListener

### TODOS
# TODO recover after crash
# TODO can something be down about the mouse snap?
# TODO Have long and short versions for commands
###

command_queue=Queue()
MOUSE_STEP=100
sock = socket.socket()
mouse = MouseController()
keyboard = KeyboardController()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

# Tab is a special case because I don't want people alt tabbing out the game
# Cealsha this means you
def press_tab():
    keyboard.release(Key.shift_l)
    keyboard.release(Key.alt)
    time.sleep(0.3)
    press_key(Key.tab)


def press_key(key):
    keyboard.press(key)
    #time.sleep(0.3)
    keyboard.release(key)

def click(key):
    mouse.press(key)
    time.sleep(0.3)
    mouse.release(k)

def mouse_down(y=''):
    mouse.position = (1,1)
    if y == '':
        mouse.move(0,MOUSE_STEP)
    elif y > 0 and y <= 3000:
        mouse.move(0,int(y))
        
def mouse_up(y=''):
    mouse.position = (1,1)
    if y == '':
        mouse.move(0,-MOUSE_STEP)
    elif y > 0 and y <= 3000:
        mouse.move(0,-int(y))

def mouse_right(x=''):
    mouse.position = (1,1)
    if x == '':
        mouse.move(MOUSE_STEP,0)
    elif x > 0 and x <= 4000:
        mouse.move(int(x), 0)

def mouse_left(x=''):
    mouse.position = (1,1)
    if x == '':
        mouse.move(-MOUSE_STEP, 0)
    elif x > 0 and x <= 4000:
        mouse.move(-int(x), 0)
        
def reset_buttons():
    mouse.release(Button.right)
    mouse.release(Button.left)
    keyboard.release('w')
    keyboard.release('s')
    keyboard.release('a')
    keyboard.release('d')
    keyboard.release('e')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.alt)

# This was for debugging
def on_move(x,y):
    pass
    #print("print('Pointer moved to {0}".format((x,y)))

def on_release(key):
    print('Released: ' + key.char)
    if key == Key.alt:
        alt_down=false

def on_press(key):
    if key == Key.F1:
        sock.close()
        logging.info("F1 Pressed. Exiting")
        print("F1 Pressed. Exiting")
        sys.exit()

def command_runner():
    while True:
        if command_queue.qsize() != 0:
            #command: (name, function, value)
            c =         command_queue.get()
            name=       c[0]
            function=   c[1]
            value=      c[2]

            logging.debug("Executed {}:{}".format(name, value))
            if value == '':
                function()
            else:
                function(value)
        else:
            pass
            
# skyrim command list 
commands = [
    # (command, function)
    ('rmb', lambda: click(Button.right)),
    ('hrmb', lambda: mouse.press(Button.right)),
    ('rrmb', lambda: mouse.release(Button.right)),
    ('lmb', lambda: click(Button.left)),
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
    ('hs', lambda: keyboard.press('s')),
    ('ha', lambda: keyboard.press('a')),
    ('hd', lambda: keyboard.press('d')),
    ('rw', lambda: keyboard.release('w')),
    ('rs', lambda: keyboard.release('s')),
    ('ra', lambda: keyboard.release('a')),
    ('rd', lambda: keyboard.release('d')),
    ('ctrl', lambda: press_key(Key.ctrl)),
    ('f', lambda: press_key('f')),
    ('clock', lambda: press_key(Key.caps_lock)),
    ('t', lambda: press_key('t')),
    ('j', lambda: press_key('j')),
    ('e', lambda: press_key('e')),
    ('tab', press_tab),
    ('r', lambda: press_key('r')),
    ('l', lambda: press_key('l')),
    ('m', lambda: press_key('m')),
    ('space', lambda: press_key(Key.space)),
    ('he', lambda: keyboard.press('e')),
    ('re', lambda: keyboard.release('e')),
    ('q', lambda: press_key('q')),
    ('esc', lambda: press_key(Key.esc)),
    ('save', lambda: press_key(Key.f5)), # Instead of F5 because parsing problems
    ('up', lambda: press_key(Key.up)),
    ('down', lambda: press_key(Key.down)),
    ('left', lambda: press_key(Key.left)),
    ('right', lambda: press_key(Key.right)),
    ('hshift', lambda: keyboard.press(Key.shift_l)),
    ('rshift', lambda: keyboard.release(Key.shift_l)),
    ('enter', lambda: press_key(Key.enter)),
    ('release', reset_buttons),
    ('moo', lambda: logging.log('Said the blue cow')),
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
    listener = KListener(on_press=on_press,
                        on_release=on_release)
    #listener.start()
    executor = Thread(target=command_runner)
    executor.start()
    print('Started command execute thread...')
    print('Beginning command parsing...')
    while True:
        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif 'Improperly formatted auth' in resp:
                print('Bad Auth Key')
                sys.exit()
            elif len(resp) > 0:
                fmtre = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp)
                if fmtre is not None:
                    username, channel, message = fmtre.groups()    
                    message = message.replace('\r', '')
                    # print(f"Channel: {channel} \nUsername: {username} \nMessage: {message}")
                    msg = re.search('^([a-zA-Z_]+)[ ]?([0-9]*)$',message)
                    if msg != None:
                        command, value = msg.groups()
                        value = int(value) if value != '' else value
                        for c in commands:
                            if command == c[0]:
                                logging.debug("Added To Queue:{}:{}:{}:{}".format(channel,username,command,value))
                                command_queue.put((c[0],c[1],value))
        except KeyboardInterrupt:
            sock.close()
            executor.join()
            logging.exception('It was you and you know it')
            print('Stopping Everything. Exiting...')
            sys.exit()
        except ConnectionError:
            sock.close()
            logging.exception('Probably Twitch...')
        except Exception as e:
            logging.exception('Fuck')

if __name__ == "__main__":
    main(sys.argv[1:])



