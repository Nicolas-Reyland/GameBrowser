# GameBrowser - Game
import tkinter as tk
from extract_icon import extract
from psutil import virtual_memory, cpu_percent
from numpy import load as load_file
from bmp import bmp_to_logo
import os, threading, time, requests, sys
import subprocess

'''
cd c:\Documents\python\projects\GameBrowser
cls & python main.pyw

'''

class Game:
	def __init__(self, path, name):

		self.exe_path = path
		self.launched = False
		self.suspended = False
		self.name = name

		self.shown = False
		self.inthread = False

	def test_icon(self):
		test = extract(self.exe_path)
		return test

	def launch(self):
		self.icon = extract(self.exe_path)
		self.show_box()
		self.launched = True
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW # startupinfo=si # creationflags=subprocess.CREATE_NO_WINDOW
		threading.Thread(target=lambda :subprocess.call('"{}"'.format(self.exe_path), startupinfo=si)).start()

	def force_stop(self):
		stdout = os.system('taskkill /IM "{}" /F'.format(os.path.basename(self.exe_path)))
		print(f'stdout: {stdout}')
		self.launched = False
		self.close_toplevel()

	def freeze_process(self):
		if not self.suspended:
			stdout = os.system('cd "{}" & pssuspend.exe "{}"'.format(os.path.join(os.getcwd(), 'PsTools'), os.path.basename(self.exe_path)))
			self.suspended = True
			self.freeze_button.configure(bg='#ccffff', activebackground='#33ccff', text='Reprendre')
		else:
			stdout = os.system('cd "{}" & pssuspend.exe -r "{}"'.format(os.path.join(os.getcwd(), 'PsTools'), os.path.basename(self.exe_path)))
			self.suspended = False
			self.freeze_button.configure(bg='#33ccff', activebackground='#ccffff', text='Suspendre')
		print(f'stdout: {stdout}')

	def show_box(self):
		self.toplevel = tk.Toplevel(width=250,height=100)
		self.toplevel.title(self.name)
		self.toplevel.resizable(False, False)
		self.toplevel.protocol('WM_DELETE_WINDOW', self.close_toplevel)

		icon = bmp_to_logo(self.icon, 95)
		icon_label = tk.Label(self.toplevel)
		icon_label.icon = icon
		icon_label['image'] = icon
		icon_label.place(relx=.01,rely=.01)

		name_label = tk.Label(self.toplevel, text=self.name, font='bold')
		name_label.place(relx=.4,rely=.01)

		ram_label = tk.Label(self.toplevel, text='RAM: -- %')
		ram_label.place(relx=.4,rely=.25)

		cpu_label = tk.Label(self.toplevel, text='CPU: -- %')
		cpu_label.place(relx=.7,rely=.25)

		internet_speed_label = tk.Label(self.toplevel, text='DL: -- Kb/s')
		internet_speed_label.place(relx=.4,rely=.45)

		force_quit_button = tk.Button(self.toplevel, text='Arret forcé', command=self.force_stop, bg='#c83232', activebackground='#ff0000')
		force_quit_button.place(relx=.7,rely=.7)

		self.freeze_button = tk.Button(self.toplevel, text='Suspendre', command=self.freeze_process, bg='#33ccff', activebackground='#ccffff')
		self.freeze_button.place(relx=.41,rely=.705)

		self.shown = True
		self.label_thread = threading.Thread(target=self.update_labels, args=(ram_label,cpu_label,internet_speed_label,lambda : self.shown))
		self.label_thread.do_run = True
		self.label_thread.start()
		self.inthread = True

	def update_labels(self, ram_label, cpu_label, internet_speed_label, isvalid):
		while isvalid() and getattr(threading.currentThread(), "do_run", True):
			try:
				ram_label['text'] = 'RAM: {} %'.format(virtual_memory().percent)
				cpu_label['text'] = 'CPU: {} %'.format(cpu_percent())
				try: internet_speed_label['text'] = 'DL: {:.2f} Kb/s'.format(downspeed())
				except: internet_speed_label['text'] = 'DL: ??? Kb/s'
				time.sleep(1)
			except tk.TclError:
				break

		self.inthread = False
		print(f'{self.name}: thread stop 1')
		print('thread exit')
		exit('exiting thread')

	def close_toplevel(self):
		self.shown=False
		self.label_thread.do_run = False
		counter = 0
		while self.label_thread.is_alive():
			print('joining thread ...')
			self.label_thread.join(timeout=1.5)
			counter += 1
			if counter == 3:
				#sys.exit('thread terminated by force after {} join attemps'.format(counter))
				break
		print('thread joined')
		print(f'{self.name} thread stop 2')
		self.toplevel.destroy()


def load_games(path):
	games = []
	if not os.path.isdir(path):
		os.mkdir(path)
		print('created path')
	for file in os.listdir(path):
		game = load_file(os.path.join(path, file), allow_pickle=True)
		game_path, name, logo = game
		games.append(Game(game_path, name))
	return games


def icons_from_games(games):
	icons = []
	for game in games:
		icons.append(extract(game.exe_path))
	return icons

def downspeed():
    url = "http://speedtest.ftp.otenet.gr/files/test100k.db"

    start = time.time()
    file = requests.get(url)
    end = time.time()

    time_difference = end - start
    file_size = int(file.headers['Content-Length'])/1000    
    return file_size / time_difference

