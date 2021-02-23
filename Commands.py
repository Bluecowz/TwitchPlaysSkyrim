from enum import Enum
class Commands(Enum):
    RIGHT_MOUSE='rm'
    HOLD_RIGHT_MOUSE='hrm'
    RELEASE_RIGHT_MOUSE='rrm'
    LEFT_MOUSE='lm'
    HOLD_LEFT_MOUSE='hlm'
    RELEASE_LEFT_MOUSE='rlm'
    MOUSE_UP='mup'
    MOUSE_DOWN='mdown'
    MOUSE_LEFT='mleft'
    MOUSE_RIGHT='mright'
    HOLD_ALT='halt'
    RELEASE_ALT='ralt'
    PRESS_Z='z'
    PRESS_W='w'
    PRESS_S='s'
    PRESS_A='a'
    PRESS_D='d'
    HOLD_W='hw'
    HOLD_S='hs'
    HOLD_A='ha'
    HOLD_D='hd'
    RELEASE_W='rw'
    RELEASE_S='rs'
    RELEASE_A='ra'
    RELEASE_D='rd'
    PRESS_CTRL='ctrl'
    PRESS_F='f'
    PRESS_CAPS_LOCK='clock'
    PRESS_T='t'
    PRESS_J='j'
    PRESS_E='e'
    PRESS_TAB='tab'
    PRESS_R='r'
    PRESS_L='l'
    PRESS_M='m'
    PRESS_SPACE='space'
    HOLD_E='he'
    RELEASE_E='re'
    PRESS_Q='q'
    # ESC='esc'
    F5='f5'
    UP_ARROW='up'
    DOWN_ARROW='down'
    LEFT_ARROW='left'
    RIGHT_ARROW='right'
    HOLD_SHIFT='hshift'
    RELEASE_SHIFT='rshift'
    ENTER='enter'
    RESET_BUTTONS='reset_buttons'
    MOO='moo'