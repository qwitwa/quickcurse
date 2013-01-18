import curses
import curses.textpad
import os
import os.path
import re
# Initialise master window and turn off character echoing
screen = curses.initscr()
curses.noecho()

#Initial variables
dims = screen.getmaxyx()
path = os.environ["HOME"]
list_of_files = os.listdir(path)
list_of_items = [] #the selection of list_of_files that are actually shown
list_pos = 0
phrase = ""
ignore_dots = True
in_topbar = False
in_leftpane = True
in_rightpane = False

#Initial screen setup:
screen.refresh()

topbar = curses.newwin(1, dims[1], 0, 0)
topbox = curses.textpad.Textbox(topbar)
topbar.bkgd(" ", curses.A_REVERSE)
topbar.refresh()

leftpane = curses.newwin(dims[0] - 2, 25, 2, 0)
leftpane.keypad(1)
leftpane.refresh()

rightpane = curses.newwin(dims[0] - 2, dims[1] - 26, 2, 26)
rightpane.addstr(0, 0, "Test")
rightpane.refresh

def update_leftpane():
	global list_of_items
	leftpane.clear()
	pos = 0
	list_of_items = []
	for name in sorted(list_of_files):
		if re.match(".*" + phrase + ".*", name) and dotfile_test(name) and os.path.isfile(path + "/" + name)  and pos < dims[0] - 2 :
			list_of_items.append(name)
			if pos == list_pos:
				leftpane.addnstr(pos, 0, name, 25, curses.A_BOLD) 
			else:
				leftpane.addnstr(pos, 0, name, 25)
			pos += 1
	leftpane.refresh()

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

#This is the main event loop. 
while True:
	if in_topbar == True:
		get_top_bar()
		list_pos = 0
		in_topbar = False
		in_leftpane = True

	update_leftpane()

	if in_rightpane == True:
		pass
	if in_leftpane == True:
		curses.napms(40)
		key = leftpane.getch()
		if key == curses.KEY_DOWN:
			if list_pos < len(list_of_items) - 1:
				list_pos += 1
		elif key == curses.KEY_UP:
			if list_pos > 0:
				list_pos -= 1
		elif key == ord("q"):
			curses.endwin()
			exit()
		elif key == 27: #escape 
			in_leftpane = False
			in_topbar = True
	screen.refresh()


