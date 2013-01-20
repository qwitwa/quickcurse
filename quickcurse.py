import curses
import curses.textpad
import os
import os.path
import re
import subprocess

# Initialise master window and turn off character echoing
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)

#Initial variables
dims = screen.getmaxyx()
path = os.environ["HOME"] + "/Dropbox/plain text"
list_of_files = os.listdir(path)
list_of_items = [] #the selection of list_of_files that are actually shown
files = {}
list_pos = 0
ignore_dots = True
focus = "left" #left or right

#Initial screen setup:
screen.refresh()

topbar = curses.newwin(1, dims[1], 0, 0)
topbar.refresh()

rightpane = curses.newwin(dims[0] - 2, dims[1] - 28, 2, 28)
rightpane.refresh()

leftpane = curses.newwin(dims[0] - 2, 25, 2, 0)
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

phrase = stringbuffer()

def update_leftpane(create = False):
	global list_of_items, files
	leftpane.clear()
	pos = 0
	list_of_items = []
	for name in sorted(list_of_files):
		if re.match("(?i).*" + phrase.stringdata + ".*" + "\.txt$", name) and notdotfile(name) and os.path.isfile(path + "/" + name)  and pos < dims[0] - 2 :
			list_of_items.append(name)
			if not name in files:
				fd_being_slurped = open(path + "/" + name)
				files[name] = fd_being_slurped.read()
			if pos == list_pos:
				leftpane.addnstr(pos, 0, name, 25, curses.A_BOLD) 
			else:
				leftpane.addnstr(pos, 0, name, 25)
			pos += 1
#	if create and len(list_of_files):
#		new_fd = open(path + "/" + phrase + ".txt", "w")
#		new_fd.write("")

	leftpane.refresh()

def update_rightpane():
	rightpane.clear()
	if list_pos in list_of_items:
		name = list_of_items[list_pos]
	else : name = ""
	if name in files:
		rightpane.addstr(0, 0, files[name])
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


update_topbar()
update_leftpane()
update_rightpane()


def get_command():
	key = leftpane.getch()
	if key == ord("q"):
		curses.endwin()
		exit()

#This is the main event loop.
while True:
	update_leftpane(True)
	list_pos = 0
	if focus == "right":
		pass
	if focus == "left":
		curses.napms(40)
		key = leftpane.getch()
		if key == curses.KEY_DOWN:
			if list_pos < len(list_of_items) -1:
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
			update_rightpane()
		elif key == 127: #backspace
			phrase.backspace()
			update_topbar()
			update_rightpane()

