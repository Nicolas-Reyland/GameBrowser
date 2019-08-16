# GameBrowser - GUIfunctions
from Game import Game
from numpy import save as save_file
from tkinter import filedialog
import tkinter as tk
import os

def search(e=0, gb):
	entry = widgets['search bar'].get()
	# ... search here
	print('searched')

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
		gb.games.append(game)
		game_logo = game.test_icon()
		save_file(os.path.join(gb.game_path, name), [game_path, name, game_logo])
		gb.redraw()

def select_game(info):
	gb, i = info
	if gb.selected is None:
		for index,button in enumerate(gb.buttons):
			if index != i:
				button.widget.configure(bg='#d9d9d9')
			else:
				button.widget.configure(bg='#46fa46')
		# colorate the start button in green
		widgets['start button'].configure(bg='#28d228', activebackground='#46fa46')
		gb.selected = gb.games[i]
	else:
		# reset all buttons
		for button in gb.buttons:
			button.widget.configure(bg='#d9d9d9')
		# gray out the start button
		widgets['start button'].configure(bg='#d9d9d9', activebackground='#ececec') # d9d9d9
		# new game selected
		if i != gb.games.index(gb.selected):
			gb.selected = None
			select_game(info)
		else:
			gb.selected = None


def start_game(gb):
	if gb.selected:
		gb.selected.launch()

def remove_game(gb):
	if gb.selected:
		if custom_askyesno('Confirmer', 'Voulez-vous vraiment retirer {} de votre liste ?'.format(gb.selected.name), width=200):
			os.remove(os.path.join(gb.game_path, gb.selected.name) + '.npy')
			gb.games.remove(gb.selected)
			gb.selected = None
			gb.redraw()
			widgets['start button'].configure(bg='#d9d9d9', activebackground='#d9d9d9') # ececec
