# TwtichPlaysSkyrim
A python script to parse twitch chat and play skyrim on the local machine. 

Currently, the game needs to be in focus while the script runs in the background. 

The chat commands are built around the idea that a user would want to do one of three things with a button: press, hold, and release. Therefore, command conventions are build around that with 'h' being the prefix for hold and 'r' being a prefix to release. And example would be 

| Command | What You Want To Do |
| --- | --- |
| he | Hold E |
| rlm | Release Left Mouse |

This formatting of commands might be confusing at first and feedback on how to improve them would be fantastic. I also want to add more verbose command names people could use instead, for example, if you want to hold the e button a user could type "he" or "Hold E". 

Mouse movements can be give an arguement for how far to move. The mouse movement is... finicky. If not specified a step is supplied. 

# Command Table

| Command | What You Want To Do |
| --- | --- |
| rmb | Click Right Mouse Button |
| hrmb | Hold Right Mouse Button |
| rrmb | Release Right Mouse Button |
| lmb | Click Left Mouse Button |
| hlmb | Hold Left Mouse Button |
| rlmb | Release Left Mouse Button |
| mup | Move The Mouse Up |
| mupX | Move The Mouse Up X pixels. Ex: mup600 |
| mdown | Move The Mouse Down |
| mdownX | Move The Mouse Down X pixels. Ex: mdown600 |
| mleft | Move The Mouse Left |
| mleftX | Move The Mouse Left X pixels. Ex: mleft600 |
| mright | Move The Mouse Right |
| mrightX | Move The Mouse Right X pixels. Ex: mright600 |
| halt | Hold Alt |
| ralt | Release Alt |
| z | Press Z |
| w | Press W |
| s | Press S |
| a | Press A |
| d | Press D |
| hw | Hold W |
| hs | Hold S |
| ha | Hold A |
| hd | Hold D |
| rw | Release W |
| rs | Release S |
| ra | Release A |
| rd | Release D |
| ctrl | Press Ctrl |
| f | Press F |
| clock | Press Caps Lock |
| t | Press T |
| j | Press J |
| e | Press E |
| tab | Press Tab |
| r | Press R |
| l | Press L |
| m | Press M |
| space | Press Space |
| he | Hold E |
| re | Release E |
| q | Press Q |
| esc | Press Esc (Removed but might add it back) |
| save | Press F5 |
| up | Press Up Arrow |
| down | Press Down Arrow |
| left | Press Left Arrow |
| right | Press Right Arrow |
| hshift | Hold Left Shift |
| rshift | Release Lift Shift |
| enter | Press Enter |
| reset_buttons | Release All Buttons, just in case |
| moo | Internal Test Command |

# Yup

Skyrim Controls can be found here: https://elderscrolls.fandom.com/wiki/Controls_(Skyrim)
 

# Whats Next?

Refine it maybe? 

I would like to be able to load configs and play multiple games thought the same script.
