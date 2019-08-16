# GameBrowser- graphics
import tkinter as tk
import widgets as widg
from os.path import isfile

widg.root.bind('<Return>', widg.GUIf.search)

save_image = lambda array,path: Image.fromarray(array, mode='RGB').save(path, format='BMP')

