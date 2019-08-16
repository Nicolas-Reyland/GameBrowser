# GameBrowser- graphics
import tkinter as tk
import GUIfunctions as GUIf
#from tkinter.ttk import Combobox
#from Game import quick_search

root = tk.Tk()
tk.Canvas(root, width=800, height=500).pack()

widgets = {'root': root}
GUIf.widgets = widgets

# - Frames -
top_frame = tk.Frame(root)
top_frame.place(relx=0,rely=.01,relwidth=1,relheight=.08)
widgets['top frame'] = top_frame

icon_frame = tk.Frame(root)
icon_frame.place(relx=0,rely=.1,relwidth=1,relheight=.9)
widgets['icon frame'] = icon_frame

bottom_frame = tk.Frame(root)
bottom_frame.place(relx=0,rely=.91,relwidth=1,relheight=.08)
widgets['bottom frame'] = bottom_frame

# - Search Bar -
search_bar = tk.Entry(top_frame, text='Rechercher un jeu ...', validatecommand=lambda : GUIf.search(gb)) # Combobox(top_frame, values=quick_search())
#search_bar.set('Rechercher un jeu ...')
search_bar.place(relx=0,rely=0,relwidth=.9,relheight=1)
search_bar.focus_set()
widgets['search bar'] = search_bar

search_button = tk.Button(top_frame, text='OK', command=lambda : GUIf.search(gb))
search_button.place(relx=.9,rely=0,relwidth=.1,relheight=1)
widgets['search button'] = search_button


# - Icon Frame -

icon_frame.update()
scrollbar = tk.Scrollbar(icon_frame)
scrollbar.place(relx=.965,rely=0,relwidth=.035,relheight=.9)
#scrollbar.place(x=icon_frame.winfo_width()-20,rely=0,width=20,relheight=.9)
widgets['scrollbar'] = scrollbar



# - Bottom Frame -
add_button = tk.Button(bottom_frame, text='Ajouter un Jeu', command=lambda : GUIf.add_game(gb))
add_button.place(relx=.05,rely=0,relwidth=.2,relheight=1)
widgets['add button'] = add_button

start_button = tk.Button(bottom_frame, text='LANCER', command=lambda : GUIf.start_game(gb)) # handle color (grayed out, etc.)
start_button.place(relx=.3,rely=0,relwidth=.4,relheight=1)
widgets['start button'] = start_button

remove_button = tk.Button(bottom_frame, text='Enlever un Jeu', command=lambda : GUIf.remove_game(gb)) # handle color (grayed out, etc.)
remove_button.place(relx=.75,rely=0,relwidth=.2,relheight=1)
widgets['remove button'] = remove_button


def custom_askyesno(title, content, affirmative='Oui', negative='Non', width=400):
	temptop = tk.Toplevel(width=width)
	temptop.title(title)
	temptop.attributes('-topmost', 'true')

	fontsize = 15
	formated_text = format_text_by_width(content, width, font_size=fontsize)
	tk.Label(temptop, text=formated_text, font='Times 15').place(relx=0,rely=0,relwidth=1,relheight=.7)

	var = tk.IntVar()
	tk.Button(temptop, text=affirmative, command=lambda : var.set(1)).place(relx=0.05,rely=.75,relwidth=.4,relheight=.2)
	tk.Button(temptop, text=negative, command=lambda : var.set(0)).place(relx=0.55,rely=.75,relwidth=.4,relheight=.2)

	temptop.configure(height=int(len(formated_text.split('\n')) * (fontsize * 1.5) + 30))

	temptop.wait_variable(var)
	temptop.destroy()

	if var.get() == 1:
		return True
	else:
		return False

def format_text_by_width(text, max_px_length, font_size=10, line_prefix=''):
	max_str_length = max_px_length / font_size
	if type(text) == str:
		text = [text]
	s = ''
	for line in text:
		if len(line) > max_str_length:
			sline = line.split()
			line, cur = [[]], 0
			for word in sline:
				if len(' '.join(line[cur])) + len(word) < max_str_length:
					line[cur].append(word)
				else:
					line.append(['\n{}{}'.format(line_prefix, word)])
					cur += 1
			line = ' '.join([word for subline in line for word in subline])

		s += line_prefix + line + '\n'

	return s

GUIf.custom_askyesno = custom_askyesno

