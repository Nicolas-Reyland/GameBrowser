# GameBrowser - GUIfunctions
from Game import Game, load_games, open_steam
from numpy import save as save_file
from tkinter import messagebox, filedialog, END # END for an entry clear
from fuzzywuzzy import fuzz
from icon import extract, bmp_to_logo
import tkinter as tk
import os, glob

def string_score(s1, s2):
	'''Returns 1 - the start-index of s2 in s1 divided by (the length of s1 - the length of s2)'''
	s1, s2 = s1.lower(), s2.lower()
	if s1 == s2: return 1
	return 1 - s1.index(s2) / (len(s1) - len(s2))

def search(gb):
	entry = widgets['search bar'].get()
	if entry.startswith('!'):
		return command_handler(entry, gb)

	# search
	min_score = .3
	ratios = [(fuzz.ratio(game.name, entry) / 100, i) for i,game in enumerate(gb.games)]
	rule_search = [(string_score(game.name, entry), i) for i,game in enumerate(gb.games) if entry.lower() in game.name.lower()]
	final_search = list(filter(lambda name: name[0] > min_score, rule_search + ratios))
	final_search.sort(key=lambda result: result[0], reverse=True) # sort after search-result relevance (pertinence)
	final_search = list(map(lambda x: x[1], final_search))
	final_search = list(set(final_search))

	gb.show_selected(final_search)

def clear_search(gb):
	gb.widg.widgets['search bar'].delete(0, END)
	search(gb)

def ask_game_name(game_path):
	toplevel = tk.Toplevel(width=200)
	toplevel.title('Nom du Jeu')
	tk.Label(toplevel, text='Nom du Jeu').grid(row=0,column=0)
	bool_var = tk.BooleanVar()
	bool_var.set(False)
	var = tk.StringVar()
	var.set(os.path.basename(game_path)[:-4])
	e = tk.Entry(toplevel, textvariable=var)
	e.grid(row=1,column=0)
	e.focus_set()
	b_ok = tk.Button(toplevel, text='OK', command=lambda : bool_var.set(True))
	b_ok.grid(row=2,column=0)
	toplevel.bind('<Return>', lambda x=0: bool_var.set(True))

	toplevel.wait_variable(bool_var)
	toplevel.destroy()

	return var.get()


def add_game(gb):
	game_paths = filedialog.askopenfilenames(initialdir='/', title='Ajouter un Jeu')
	for game_path in game_paths:
		name = ask_game_name(game_path)
		game = Game(game_path, name)
		gb.add_games([[game_path, name]])
		game_icon = game.test_icon()
		save_file(os.path.join(gb.game_path, name), [game_path, name, game_icon])
		gb.redraw()

def select_game(info):
	if len(info) == 2:
		gb, i = info
		button_index = i
	elif len(info) == 3:
		gb, i, button_index = info
	else:
		raise ValueError('{} is not a valid length for info!'.format(len(info)))
	if gb.selected is None:
		for index,button in enumerate(gb.buttons):
			if index != button_index: # not selected
				button.widget.configure(bg='#d9d9d9')
				gb.name_labels[index].configure(fg='#000000')
			else: # selected
				button.widget.configure(bg='#46fa46', activebackground='#28d228')
				gb.name_labels[button_index].configure(fg='#28d228')
		# colorate the start button in green
		widgets['start button'].configure(bg='#28d228', activebackground='#46fa46')
		gb.selected = gb.games[i]
	else:
		# reset all buttons
		for button in gb.buttons:
			button.widget.configure(bg='#d9d9d9')
		for label in gb.name_labels:
			label.configure(fg='#000000')
		# gray out the start button
		widgets['start button'].configure(bg='#d9d9d9', activebackground='#ececec') # d9d9d9
		# new game selected
		if i != gb.games.index(gb.selected):
			gb.selected = None
			select_game(info)
		else:
			gb.selected = None


def start_game(gb):
	if gb.settings.settings['CLOSE_MAIN_AT_LAUNCH']:
		gb.widg.root.withdraw()
	if gb.selected:
		gb.selected.launch(gb.widg.root, gb.settings.settings['SHOW_BOX'], gb.settings.settings['TOPMOST_BOX'], info=gb.settings.settings['CLOSE_MAIN_AT_LAUNCH'])

def remove_game(gb):
	if gb.selected:
		if messagebox.askyesno('Confirmer', 'Voulez-vous vraiment retirer {} de votre liste ?'.format(gb.selected.name)):
			os.remove(os.path.join(gb.game_path, gb.selected.name) + '.npy')
			gb.games.remove(gb.selected)
			gb.selected = None
			gb.redraw()
			widgets['start button'].configure(bg='#d9d9d9', activebackground='#d9d9d9') # ececec

def command_handler(command, gb):
	assert command.startswith('!')
	command = command[1:]

	if command == 'reload_all':
		gb.games = []
		games = load_games(gb.game_path)
		game_path = gb.game_path
		gb.__init__(games, game_path)
		gb.redraw()
		return
	elif command == 'steam':
		open_steam()
		return
	elif command == 'exit':
		gb.close_root()
	elif command == 'help':
		print('not done yet: !{}'.format(command))
		return

	# is there and arguemt ?
	if len(command.split()) < 2:
		return

	module = command.split()[0]

	# filter the args out
	args = command[len(module)+1:]

	# choose module
	if module == 'scanner':
		if args == 'steam':
			gb.scanner.scan_steam()

		if args == 'openfolder':
			gb.scanner.openfolder()

		if args.startswith('"') and args.endswith('"'):
			argpath = args[1:-1]
			if os.path.isdir(argpath):
				gb.scanner.scan_dir(argpath)

	if module == 'edit':
		if args.startswith('rename '):
			args = args.replace('rename ', '')
			if args.startswith('"') and args.endswith('"') and '" "' in args and args.count('"') == 4:
				arg1 = args[1:args[1:].index('"')+1]
				arg2 = args[args.index('" "')+3:-1]
				gb.edit.rename(Game, arg1, arg2)
				command_handler('!reload_all', gb)
				gb.redraw()

		if args.startswith('exefile'):
			gb.edit.edit_exefile(args)

	if module == 'settings':
		if len(args.split()) == 2:
			boolarg = args.split()[1]

			if boolarg in ['true', 'True', 'TRUE', '1', 'false', 'False', 'FALSE', '0']:

				if args.startswith('CLOSE_MAIN_AT_LAUNCH'):
					gb.settings.set('CLOSE_MAIN_AT_LAUNCH', boolarg)

				if args.startswith('SHOW_BOX'):
					gb.settings.set('SHOW_BOX', boolarg)

				if args.startswith('START_STEAM_AT_STEAM_GAMES'):
					gb.settings.set('START_STEAM_AT_STEAM_GAMES', boolarg)

				if args.startswith('TOPMOST_BOX'):
					gb.settings.set('TOPMOST_BOX', boolarg)

		if args == 'show': # then it's not a boolean arg, but idk
			messagebox.showinfo('Info', gb.settings.settings)




