# GameBrowser - Game
import tkinter as tk
from icon import extract, bmp_to_logo
from psutil import virtual_memory, cpu_percent
from numpy import load as load_file
# from screeninfo import get_monitors
from win32api import GetMonitorInfo, MonitorFromPoint
import os, threading, time, requests, sys
import subprocess

r'''
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

	def launch(self, root):
		self.root = root
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
		self.root.deiconify()

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

	def geometry(self, corner):
		# monitor = get_monitors()[0] # multi-monitor support ...
		self.toplevel.update()
		width = self.toplevel.winfo_width()
		height = self.toplevel.winfo_height()
		# x = 0 # monitor.width - width
		# y = monitor.height - height
		monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
		monitor_area = monitor_info.get('Monitor')
		work_area = monitor_info.get('Work')
		taskbar = (monitor_area[2]-work_area[2], monitor_area[3]-work_area[3])
		print('taskbar',taskbar)
		x = 0 + taskbar[0] - 10
		y = monitor_area[3] - height - taskbar[1] - 32
		print('monitor',monitor_area)
		print('work',work_area)

		geometry = '{}x{}+{}+{}'.format(width, height, x, y)
		print('geometry', geometry)
		self.toplevel.geometry(geometry)

	def show_box(self):
		self.toplevel = tk.Toplevel(width=250,height=100)
		self.geometry('bottom left') # places the toplevel at a corner
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
				print('join failed after {} attempts. Forcing thread extinction'.format(counter))
				break
		print('thread joined')
		print(f'{self.name} thread stop 2')
		self.toplevel.destroy()
		self.root.deiconify()


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

