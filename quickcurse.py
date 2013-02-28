# Something strange is happening when scrolling, only allowing scroll through 2 list items. 
import curses
import curses.textpad
import os
import os.path
import re
import subprocess

# Initialise master window, turn off character echoing, and disable the cursor.
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)

#Initial variables
dims = screen.getmaxyx() #tuple containing the maximum screen dimensions.
path = os.environ["HOME"] + "/Dropbox/plain text" #set the path to get notes from.
list_of_files = os.listdir(path) #grab the names of all the files in the specified path
list_of_items = [] #the selection of list_of_files that are actually shown
files = {} #contains the content of every file ever shown
files["default"] = "Well, here's some default content"
list_pos = 0
ignore_dots = True #Toggle hidden files
focus = "left" #left or right

#Initial screen setup:
screen.refresh()

topbar = curses.newwin(1, dims[1], 0, 0) #the bar to type in
topbar.refresh()

rightpane = curses.newwin(dims[0] - 2, dims[1] - 28, 2, 28) #the pane for showing note content
rightpane.refresh()

leftpane = curses.newwin(dims[0] - 2, 25, 2, 0) #the pane for showing note names
leftpane.keypad(1)
leftpane.refresh()

class stringbuffer:
	def __init__(self, contents = ""):
		self.stringdata = contents
	def append(self, string_to_append ):
		self.stringdata = self.stringdata + string_to_append
	def backspace(self):
		length = len(self.stringdata)
		self.stringdata = self.stringdata[:length - 1]


def update_leftpane():
	global list_of_items, files
	leftpane.clear()
	pos = 0
	list_of_items = []
	for name in sorted(list_of_files):
		if re.match("(?i).*" + phrase.stringdata + ".*" + "\.txt$", name) and notdotfile(name) and os.path.isfile(path + "/" + name) and pos < dims[0] - 2 :
			list_of_items.append(name)
			if not name in files:
				fd_being_slurped = open(path + "/" + name)
				files[name] = fd_being_slurped.read()
			if pos == list_pos:
				leftpane.addnstr(pos, 0, name, 25, curses.A_BOLD) 
			else:
				leftpane.addnstr(pos, 0, name, 25)
			pos += 1
	leftpane.refresh()



def update_rightpane():
	rightpane.clear()
	if list_pos < len(list_of_items):
		name = list_of_items[list_pos]
	else: name = "default"
	if name in files:
		rightpane.addstr(0, 0, debug() + files[name])
	rightpane.refresh()

def update_topbar():
	topbar.clear()
	topbar.addstr(0, 0, phrase.stringdata)
	topbar.refresh()

def notdotfile(name):
	if not ignore_dots:
		return True
	elif re.match("^\..*", name):
		return False
	else:
		return True

def get_command(): # These two functions are unnecessarily fancy. "Get" prints a command prompt and waits for a key, "Show" prints the command and waits for enter or cancelation.
	topbar.clear()
	topbar.addstr(0, 0, "command: ")
	topbar.refresh()
	key = leftpane.getch()
	if key == ord("q"):
		if show_command("quit"):
			curses.endwin()
			exit()
	topbar.clear()
	topbar.addstr(0, 0, phrase.stringdata)
	topbar.refresh()

def show_command(command):
	topbar.addstr(0, 9, command[:1], curses.A_BOLD)
	topbar.addstr(0, 10, command[1:])
	topbar.refresh()
	key = topbar.getch()
	if key == 10:
		return True
	else:
		return False

def debug():
	debug_text = "(File table length: " + str(len(files)) + ") (list_pos: " + str(list_pos) + ") (list_of_items length: " + str(len(list_of_items)) + ")\n\n"
	return debug_text

phrase = stringbuffer()

#This is the main event loop.
while True:
	update_leftpane()
	update_rightpane()
	list_pos = 0
	if focus == "right":
		pass
	if focus == "left":
		key = leftpane.getch()
		if key == curses.KEY_DOWN:
			if list_pos < len(list_of_items) - 2 :
				list_pos += 1
				update_rightpane()
		elif key == curses.KEY_UP:
			if list_pos > 0:
				list_pos -= 1
				update_rightpane()
		elif key == ord(":"):
			get_command()
		elif re.match("[A-Za-z0-9]", chr(key)):
			phrase.append(chr(key))
			update_topbar()
			update_leftpane()
			update_rightpane()
		elif key == 127: #backspace
			phrase.backspace()
			update_topbar()
			update_leftpane()
			update_rightpane()

