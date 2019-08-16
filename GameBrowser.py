# GameBrowser - GameBrowser
from graphics import widg
from icon import bmp_to_logo
from Game import icons_from_games
from CustomTkWidget import CustomTkWidget
import sys

class GameBrowser:
	def __init__(self, games, game_path):

		self.games = games
		self.game_path = game_path
		self.widg = widg
		self.widg.gb = self

		self.icons = icons_from_games(self.games)
		self.buttons = []
		self.selected = None
		self.create_icons()

		self.widg.root.bind('<Return>', lambda _:widg.GUIf.search(self))

	def get_imwidth(self, l):
		self.widg.widgets['icon frame'].update()
		imwidth = self.widg.widgets['icon frame'].winfo_width()
		imwidth *= .965 - .025
		imwidth /= l
		imwidth = int(imwidth)
		return imwidth

	def show_selected(self, index_list):
		selected_games = [self.games[index] for index in index_list]
		selected_icons = icons_from_games(selected_games)
		l = len(self.icons)
		imwidth = self.get_imwidth(l)

		relwidth, relheight = self.create_icons()
		width = self.widg.widgets['icon frame'].winfo_width() * relwidth
		height = self.widg.widgets['icon frame'].winfo_height() * relheight

		# reset icon frame & buttons
		self.reset_graphics()

		# draw
		for i,game in enumerate(selected_games):

			name_label = self.widg.tk.Label(self.widg.widgets['icon frame'], text=game.name)
			name_label.place(relx=.015+(i%7)*(.94/min(l,7)), rely=.025 + (i//7) * (.85/(l//7+1)), relwidth=.995/l, relheight=.05)

			logo = bmp_to_logo(selected_icons[i], imwidth)

			widget = CustomTkWidget(self.widg.widgets['icon frame'], 0, self.widg.GUIf.select_game)
			widget.info = [self, index_list[i], i]
			widget.widget.logo = logo # 														   width=imwidth
			widget.widget.place(relx=.015+(i%7)*(.94/min(l,7)), rely=.1 + (i//7) * (.85/(l//7+1)), width=width, height=height)
			widget.widget['image'] = logo

			self.buttons.append(widget)

	def create_icons(self):
		if len(self.games) != len(self.icons):
			self.icons = icons_from_games(self.games)
		if self.icons:
			l = len(self.icons)
			self.widg.widgets['icon frame'].update()
			imwidth = self.get_imwidth(l)

			for i,file in enumerate(self.icons):

				name_label = self.widg.tk.Label(self.widg.widgets['icon frame'], text=self.games[i].name)
				name_label.place(relx=.015+(i%7)*(.94/min(l,7)), rely=.025 + (i//7) * (.85/(l//7+1)), relwidth=.995/l, relheight=.05)

				logo = bmp_to_logo(file, imwidth)

				widget = CustomTkWidget(self.widg.widgets['icon frame'], 0, self.widg.GUIf.select_game)
				widget.info = [self, i]
				widget.widget.logo = logo # 														   width=imwidth
				widget.widget.place(relx=.015+(i%7)*(.94/min(l,7)), rely=.1 + (i//7) * (.85/(l//7+1)), relwidth=.995/l, relheight=.85/(l//7+1) - .1)
				widget.widget['image'] = logo

				self.buttons.append(widget)

			return .995/l, .85/(l//7+1) - .1
		else:
			self.widg.tk.Label(self.widg.widgets['icon frame'], text='Aucun Jeu').pack()
		return 0, 0

	def reset_graphics(self):
		# destroy all children of the icon frame
		for child in self.widg.widgets['icon frame'].winfo_children():
			child.destroy()
		# redraw
		self.buttons = []
		self.widg.widgets['start button'].configure(bg='#d9d9d9', activebackground='#ececec')

	def redraw(self):
		self.reset_graphics()
		return self.create_icons()

	def close_root(self, root):
		# close all toplevels + their threads
		for game in self.games:
			if game.shown:
				game.close_toplevel()
		# close root window
		root.destroy()
		# close program
		sys.exit('sys.exit')

	def mainloop(self):
		self.widg.root.protocol('WM_DELETE_WINDOW', lambda :self.close_root(self.widg.root))
		self.widg.root.mainloop()
