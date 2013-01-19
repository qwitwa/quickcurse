import curses
import curses.textpad
import os
import os.path
import re

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
phrase = ""
ignore_dots = True
focus = "left" #top, left or right

#Initial screen setup:
screen.refresh()

topbar = curses.newwin(1, dims[1], 0, 0)
topbox = curses.textpad.Textbox(topbar)
topbar.bkgd(" ", curses.A_REVERSE)
topbar.refresh()

rightpane = curses.newwin(dims[0] - 2, dims[1] - 28, 2, 28)
rightpane.refresh()

leftpane = curses.newwin(dims[0] - 2, 25, 2, 0)
leftpane.keypad(1)
leftpane.refresh()


def update_leftpane(create = False):
	global list_of_items, files
	leftpane.clear()
	pos = 0
	list_of_items = []
	for name in sorted(list_of_files):
		if re.match("(?i).*" + phrase + ".*" + "\.txt$", name) and dotfile_test(name) and os.path.isfile(path + "/" + name)  and pos < dims[0] - 2 :
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
	global list_of_items, files
	name = list_of_items[list_pos]
	rightpane.clear()
	#tempwin = curses.newpad(1000, dims[1] - 28)
	#tempwin.addstr(0, 0, files[name])
	#tempwin.refresh(0, 0, 2, 28, dims[0], dims[1])
	rightpane.addstr(0, 0, files[name])
	rightpane.refresh()


def dotfile_test(name):
	if not ignore_dots:
		return True
	elif re.match("^\..*", name):
		return False
	else:
		return True

def get_top_bar():
	global phrase
	phrase = str.rstrip(topbox.edit())
	if phrase == ":exit":
		curses.endwin()
		exit()
	topbar.refresh()

update_leftpane()
update_rightpane()

#This is the main event loop.
while True:
	if focus == "top":
		get_top_bar()
		update_leftpane(True)
		list_pos = 0
		focus = "left"
	update_leftpane()

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
		elif key == ord("q"):
			curses.endwin()
			exit()
		elif key == 27 or ord("l"): #escape 
			focus = "top"

