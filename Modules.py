# GameBrowser - Modules
import tkinter as tk
from tkinter import filedialog, messagebox
from fuzzywuzzy import fuzz
from icon import extract, bmp_to_logo
from CustomTkWidget import CustomTkWidget
from file_handler import save_file
import os, glob, threading
import win32api, pywintypes
import json


class Scanner:

	def __init__(self, gb):
		self.gb = gb

	def scan_steam(self): # NOT DONE YET
		games_found = []
		steam_read = False
		base_path = os.getcwd()
		if not messagebox.askokcancel('Arrêt de Steam', 'Si le programme Steam est actif, il va être fermé. Veuillez également fermer vos jeux Steam (cela fera probablement crasher le scan). Voulez-vous continuer ?'):
			return
		#messagebox.showwarning('Attention', 'Veuillez retirer tout moyen de stockage externe (USB, SSD, CD, etc) afin qu\'ils ne soient pas scannés, à moins que cela soit votre souhait. Vous pourrez arrêter le scan à tout moment.')

		os.system('taskkill /IM "Steam.exe" /F')

		drives = win32api.GetLogicalDriveStrings()
		drives = drives.split('\000')[:-1]
		for drive in drives:
			try:
				os.chdir(drive)
				if 'Program Files (x86)' in os.listdir(drive):
					os.chdir('Program Files (x86)')
					if 'Steam' in os.listdir(os.getcwd()):
						os.chdir('Steam\\steamapps\\common')
						for potential_game in os.listdir(os.getcwd()):
							print('pot', potential_game)
							sub_games = glob.glob('{}\\*.exe'.format(potential_game))

							if any([valid_file_name(os.path.basename(sub_game), potential_game) for sub_game in sub_games]):
								for sub_game in sub_games:
									if valid_file_name(os.path.basename(sub_game), potential_game):
										game_path = os.path.join(os.getcwd(), sub_game)
										games_found.append(game_path)

							else:
								for sub_game in sub_games:
									game_path = os.path.join(os.getcwd(), sub_game)
									games_found.append(game_path)

			except PermissionError:
				pass # messagebox.showerror('Erreur', f'Le lecteur {drive} n\'a pas pu être accédé. Le scan va continuer...')
		os.chdir(base_path)
		# Afficher tableau pour changer le nom et confirmer l'ajout avec une case à cocher, etc.
		games = validation_table(self.gb, games_found)
		self.gb.add_games(games)

	def openfolder(self):
		folderpath = filedialog.askdirectory(initialdir='/', title='Scanner un dossier')
		if folderpath:
			self.scan_dir(folderpath)

	def scan_dir(self, dirpath):
		base_path = self.gb.base_path
		assert base_path == os.getcwd()

		potential_games = []
		filled_paths = [] # paths where nothing is to be found anymore

		os.chdir(dirpath)
		walk = list(os.walk(dirpath))
		for path, folder, files in walk:

			if any([filled_path in path for filled_path in filled_paths]):
				continue

			for file in files:
				if valid_file_name(file, path) and path not in filled_paths:
					potential_games.append(os.path.join(path, file))
					filled_paths.append(path)

		for game in potential_games: print('potential game', os.path.basename(game))

		os.chdir(base_path)

		games = validation_table(self.gb, potential_games)
		self.gb.add_games(games)




class Edit:

	def __init__(self, gb):
		self.gb = gb

	def rename(self, Game, game_name, new_name):
		if new_name in [game.name for game in self.gb.games]:
			return
		if game_name in [game.name for game in self.gb.games]:
			game_index = [game.name for game in self.gb.games].index(game_name)
			base_game = self.gb.games[game_index]
			self.gb.games.pop(game_index)
			new_game = Game(base_game.exe_path, new_name)
			os.remove(os.path.join(os.getcwd(), self.gb.game_path, base_game.name + '.npy'))
			game_icon = new_game.test_icon()
			save_file(os.path.join(self.gb.game_path, new_name), {'exe path': new_game.exe_path, 'name': new_name, 'icon': game_icon})

	def edit_exefile(self, args):
		print('not done yet: edit_exefile')
		pass


class Settings: # SETTINGS NOT ALL IMPLEMENTED YET

	def __init__(self, gb):
		self.gb = gb
		self.settings_path = self.gb.settings_path
		self.load_settings()

	def load_settings(self):
		if not os.path.isfile(self.settings_path):
			os.mkdir(self.settings_path.replace(os.path.basename(self.settings_path), ''))
			self.settings = {'CLOSE_MAIN_AT_LAUNCH': True,
							 'SHOW_BOX': True,
							 'START_STEAM_AT_STEAM_GAMES': False, # not iplemented
							 'TOPMOST_BOX': True,
							 'SAFE_MODE': True,
							 'CLOSE_SUPP_WINDOW_AT_PID_LOST': True}
			self.write()

		else:
			with open(self.settings_path, 'rb') as file:
				self.settings = json.load(file)

	def write(self):
		with open(self.settings_path, 'w') as file:
			json.dump(self.settings, file)

	def set(self, key, value):
		# assign real boolean to 'value'
		value = value in ['true', 'True', 'TRUE', '1']
		# set the value in settings-dict
		if key in self.settings.keys():
			self.settings[key] = value

		# write new settings to disk
		self.write()
		# confirm to user
		messagebox.showinfo('Info', 'Le paramètre a été changé')


def valid_file_name(file, path):

	if not file.endswith('.exe'):
		return False

	file = file[:-4] # remove the '.exe'

	if file.lower() in os.path.basename(path).lower():
		return True

	if 'unins' in file:
		return False
	ratio = fuzz.ratio(os.path.basename(path), file) / 100

	if 'launcher' in file.lower():
		index = file.lower().index('launcher')
		newfile = file.replace(file[index:index+len('launcher')], '')
		print(f'from {file} to {newfile}')
		if len(newfile) > 1:
			if newfile.lower() not in os.path.basename(path).lower():
				print(f'ratio between {newfile} and {os.path.basename(path)} = {fuzz.ratio(newfile, os.path.basename(path)) / 100}')
				if fuzz.ratio(newfile, os.path.basename(path)) / 100 < .5:
					return False

	elif ratio < .5:
		return False

	return True

def validation_table(gb, games):
	# shows a table, with "the icon, the game name, an add button" for all found games
	global added_games, buttons, entries
	added_games, buttons, entries = [], [], []

	icons = list(map(extract, games))
	icons = list(map(lambda icon: bmp_to_logo(icon, 32), icons))

	toplevel = tk.Toplevel()
	toplevel.title('Résultat du scan')
	toplevel.resizable(False, False)
	toplevel.protocol('WM_DELETE_WINDOW', lambda : close_toplevel(toplevel))

	tk.Label(toplevel, text='Résultat du scan:', font='Times 15').grid(row=0,column=0,columnspan=3)

	for i in range(len(games)): # +1 because the 0s row is already taken

		icon_label = tk.Label(toplevel, image=icons[i])
		icon_label.icon = icons[i]
		icon_label.grid(row=i+1,column=0)

		entry = CustomTkWidget(toplevel, i, None, TkWidget=tk.Entry, use_callback=False)
		entry.widget.insert(0, os.path.basename(games[i])[:-4])
		entry.widget.grid(row=i+1,column=1)
		entries.append(entry)

		add_button = CustomTkWidget(toplevel, i, lambda i: add_game(i, games), **{'text': 'Ajouter'})
		add_button.widget.grid(row=i+1,column=2)
		buttons.append(add_button)

	confirm_var = tk.BooleanVar()
	confirm_var.set(False)
	confirm_button = tk.Button(toplevel, text='Confirmer', command=lambda : confirm_var.set(True))
	confirm_button.grid(row=i+2, column=0, columnspan=3)

	# wait for the confirm-button
	toplevel.wait_variable(confirm_var)

	# update the names (could have been changed after the adding...)
	added_game_paths = list(map(lambda game: game[0], added_games))
	for i in range(len(games)):
		if games[i] in added_game_paths:
			added_games[added_game_paths.index(games[i])][1] = entries[i].widget.get()

	print(f'final added games: {added_games}')

	# destroy the toplevel
	toplevel.destroy()

	return added_games

def add_game(i, games):
	global added_games, buttons, entries
	if buttons[i].callback_count % 2 == 0: # was not clicked - green out
		buttons[i].widget.configure(bg='#28d228', activebackground='#46fa46')
		added_games.append( [games[i], entries[i].widget.get()] ) # add game
	else: # was already clicked - gray out
		buttons[i].widget.configure(bg='#ececec', activebackground='#d9d9d9')
		print('searching in', list(map(lambda game: game[0], added_games)))
		added_games.pop(list(map(lambda game: game[0], added_games)).index(games[i])) # remove game
	print('added games',added_games)

def close_toplevel(toplevel):
	global buttons
	for child in toplevel.winfo_children():
		child.destroy()
	toplevel.destroy()

def open_steam():
	base_path = os.getcwd()
	drives = win32api.GetLogicalDriveStrings()
	drives = drives.split('\000')[:-1]
	for drive in drives:

		try: os.chdir(drive)
		except PermissionError: continue

		try:
			if 'Program Files (x86)' in os.listdir(drive):
				os.chdir('Program Files (x86)')
				if 'Steam' in os.listdir(os.getcwd()):
					os.chdir('Steam')
					threading.Thread(target=lambda : os.system('Steam.exe')).start()
					print('all good')
		except Exception as e:
			messagebox.showerror('Erreur', 'Une erreur s\'est produite lors de l\'ouverture de Steam: {}'.format(e))
	os.chdir(base_path)

class HelpModule:
	global_help_text = '''Commands:
 - reload_all
 - steam
 - scanner
 - edit
 - settings
 - exit
 - help

Ecrire "!help {commande}" pour avoir des information supplémentaires sur une commande'''

	commands_usage = {
							'reload_all': 'Recharge tous les jeux (à utiliser principalement pour recharger les graphismes)',

							'steam': 'Ouvre steam (utile pour lancer les jeux steams)',

							'scanner': '''Le mot-clé "scanner" désigne un module.
Commandes scanner:
 - steam: Scanne vos jeux steam
 - openfolder: Choisi un dossier, puis le scanne
 - (rien): Si vous voulez scanner un dossier, vous pouvez
    entrer son chemin d'accès entre guillemets '"'.
    Par exemple: '!scanner "C:\\Chemin\\vers\\le\\dossier"'.''',

							'edit': '''Le mot-clé "edit" désigne un module.
Commandes edit:
 - rename [!edit rename "{ancien-nom}" "{nouveau-nom}"]
 - exefile [!edit exefile "{nom-du-jeu}"] (pas encore fait)''',

							'settings': '''Le mot-clé "settings" désigne un module.
Voici les paramètres changeables:
 - CLOSE_MAIN_AT_LAUNCH
 - SHOW_BOX
 - START_STEAM_AT_STEAM_GAMES
 - TOPMOST_BOX
 - CLOSE_SUPP_WINDOW_AT_PID_LOST
Utilisation: [!settings {nom-de-param} {nouvelle-valeur}]
Les valeurs possibles sont {0, 1, true, false, TRUE, FALSE}''',

							'exit': 'Fermer le programme.',

							'help': "Montre ce message d'aide."
						 }
