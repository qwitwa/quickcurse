import curses
import curses.textpad
import os
import re
# Initialise master window and turn off character echoing
screen = curses.initscr()
curses.noecho()
ignore_dots = True

#Initial variables
dims = screen.getmaxyx()
list_of_files = os.listdir(os.environ["HOME"] + "")
phrase = ""

#Initial screen setup:
screen.hline(1, 0, "=", dims[1]) 	#Draw a horizontal line under the top bar
screen.vline(2, 26, "|", dims[0] -2 )
screen.refresh()

topbar = curses.newwin(1, dims[1], 0, 0)#Create a one line window at the top
topbox = curses.textpad.Textbox(topbar)	#Using the just created window, create a textbox

leftpane = curses.newwin(dims[0] - 2, 25, 2, 0) #Create left pane window under what has gone before
leftpane.refresh()

def update_leftpane():
	leftpane.clear()
	pos = 0
	for name in sorted(list_of_files):
		if re.match(".*" + phrase + ".*", name) and dotfile_test(name) and pos < dims[0] - 2 :
			leftpane.addnstr(pos, 0, name, 25 )
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

#This is temporarily the main event loop. 
while True:
	update_leftpane()
	get_top_bar()
	screen.refresh()

#This is where things get complicated. We need to implement a validator function on that textbox input, so that:
#	+ Pressing enter works correctly (submits the text, and then deletes the textbox contents - at the moment the former is true but not the latter)
#	+ Backspaces work correctly 


