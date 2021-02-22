import socket 
import logging
import re
import sys
import getopt
import os
import time
from Commands import Commands
from enum import Enum
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController, Listener

### TODOS
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

def on_move(x,y):
    print("print('Pointer moved to {0}".format((x,y)))

def ParseCommand(command,value,username, channel):
    if command == Commands.RIGHT_MOUSE: # Click Right Mouse
        mouse.press(Button.right)
        time.sleep(0.3)
        mouse.release(Button.right)
    elif command == Commands.HOLD_RIGHT_MOUSE: # Hold Right Mouse
        mouse.press(Button.right)
    elif command == Commands.RELEASE_RIGHT_MOUSE: # Release Right Mouse
        mouse.release(Button.right)
    elif command == Commands.LEFT_MOUSE: # Click Left Mouse
        mouse.press(Button.left)
        time.sleep(0.3)
        mouse.release(Button.left)
    elif command == Commands.HOLD_LEFT_MOUSE: # Hold Left Mouse
        mouse.press(Button.left)
    elif command == Commands.RELEASE_LEFT_MOUSE: # Release Left Mouse
        mouse.release(Button.left)
    elif command == Commands.MOUSE_UP: # Move Mouse Up
        mouse.position = (1,1)
        if value != '':
            mouse.move(0,-int(value))
        else:
            mouse.move(0,-MOUSE_STEP)
    elif command == Commands.MOUSE_DOWN: # Move Mouse Down
        mouse.position = (1,1)
        if value != '':
            mouse.move(0,int(value))
        else:
            mouse.move(0,MOUSE_STEP)
    elif command == Commands.MOUSE_LEFT: # Move Mouse Left
        mouse.position = (1,1)
        if value != '':
            mouse.move(-int(value), 0)
        else:
            mouse.move(-MOUSE_STEP, 0)
    elif command == Commands.MOUSE_RIGHT: # Move Mouse Right
        mouse.position = (1,1)
        if value != '':
            mouse.move(int(value), 0)
        else:    
            mouse.move(MOUSE_STEP,0)
    elif command == Commands.HOLD_ALT: # Hold Alt
        keyboard.press(Key.alt)
    elif command == Commands.RELEASE_ALT: # Release Alt
        keyboard.release(Key.alt)
    elif command == Commands.PRESS_Z: # Press Z
        keyboard.press('z')
        keyboard.release('z')
    elif command == Commands.PRESS_W: # Press W
        keyboard.press('w')
        keyboard.release('w')
    elif command == Commands.PRESS_S: # Press S
        keyboard.press('s')
        keyboard.release('s')
    elif command == Commands.PRESS_A: # Press A
        keyboard.press('a')
        keyboard.release('a')
    elif command == Commands.PRESS_D: # Press D
        keyboard.press('d')
        keyboard.release('d')
    elif command == Commands.HOLD_W: # Hold W
        keyboard.press('w')
    elif command == Commands.HOLD_A: # Hold A
        keyboard.press('a')
    elif command == Commands.HOLD_S: # Hold S
        keyboard.press('s')
    elif command == Commands.HOLD_D: # Hold D
        keyboard.press('d')
    elif command == Commands.RELEASE_W: # Release W
        keyboard.release('w')
    elif command == Commands.RELEASE_A: # Release A
        keyboard.release('a')
    elif command == Commands.RELEASE_S: # Release S
        keyboard.release('s')
    elif command == Commands.RELEASE_D: # Release D
        keyboard.release('d')
    elif command == Commands.PRESS_CTRL: # Press Ctrl
        keyboard.press(Key.ctrl)
        keyboard.release(Key.ctrl)
    elif command == Commands.PRESS_F:  # Press F (to pay respect?)
        keyboard.press('f')
        keyboard.release('f')
    elif command == Commands.PRESS_CAPS_LOCK: # Press Caps Lock
        keyboard.press(Key.caps_lock)
        keyboard.release(Key.caps_lock)
    elif command == Commands.PRESS_T: # Press T
        keyboard.press('t')
        keyboard.release('t') 
    elif command == Commands.PRESS_J: # Press J
        keyboard.press('j')
        keyboard.release('j')
    elif command == Commands.PRESS_E: # Press E
        keyboard.press('e')
        keyboard.release('e')
    elif command == Commands.PRESS_TAB: # Press Tab
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif command == Commands.PRESS_R: # Press R
        keyboard.press('r')
        keyboard.release('r')
    elif command == Commands.PRESS_L: # Press L
        keyboard.press('l')
        keyboard.release('l')
    elif command == Commands.PRESS_M: # Press M
        keyboard.press('m')
        keyboard.release('m')
    elif command == Commands.PRESS_SPACE: # Press Space
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif command == Commands.HOLD_E: # Hold E
        keyboard.press('e')
    elif command == Commands.RELEASE_E: # Release E
        keyboard.release('e')
    elif command == Commands.PRESS_Q: # Press Q
        keyboard.press('q')
        keyboard.release('q')
    elif command == Commands.ESC: # Press Escape
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif command == Commands.F5: # Press F5
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif command == Commands.UP_ARROW: # Press Up
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif command == Commands.DOWN_ARROW: # Press Down
        keyboard.press(Key.down)
        keyboard.press(Key.down)
    elif command == Commands.LEFT_ARROW: # Press Left
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif command == Commands.RIGHT_ARROW: # Press Right
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif command == Commands.HOLD_SHIFT: # Hold Shift
        keyboard.press(Key.shift_l)
    elif command == Commands.RELEASE_SHIFT: # Release Shift
        keyboard.release(Key.shift_l)
    elif command == Commands.ENTER: # Press Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif command == Commands.RESET_BUTTONS: # Resets on Held Buttons
        mouse.release(Mouse.right)
        mouse.release(Mouse.left)
        keyboard.release('w')
        keyboard.release('s')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release(key.alt)
        keyboard.release('e')
        keyboard.release(Key.shift_l)
        keyboard.release(Key.alt)
    elif command == Commands.MOO: #Test Command
        print('Said The Blue Cow')


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

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    listener = Listener(on_move=on_move)
    # listener.start()

    Command_List = [item.value for item in Commands]

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
                    if message in Command_List:
                        commands = re.search('([a-zA-Z]*)([0-9]*)',message)
                        command, value = commands.groups()
                        ParseCommand(command, value, username, channel)
                        logging.debug("{}:{}:{}:{}".format(channel,username,command,value))
    except KeyboardInterrupt:
        sock.close()
        print('Socket Closed')
    except ConnectionError:
        sock.close()
        print('Connection Error')

if __name__ == "__main__":
    main(sys.argv[1:])



