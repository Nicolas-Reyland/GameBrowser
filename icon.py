# GameBrowser - extract icon
import win32ui
import win32gui
import win32con
import win32api

from cv2 import imread, cvtColor, COLOR_RGB2BGR as colorfunc
import os

from PIL import Image, ImageTk

def bmp_to_logo(file, imwidth):
    if type(file) == str:
        if isfile(file):
            image = Image.open(file + '.bmp')
    else:
        image = Image.fromarray(file)
    image = image.resize((imwidth, imwidth))
    logo = ImageTk.PhotoImage(image=image)
    return logo

def extract(path, name='save'):

    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

    large, small = win32gui.ExtractIconEx(path,0)
    win32gui.DestroyIcon(large[0])

    hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_x )
    hdc = hdc.CreateCompatibleDC()

    hdc.SelectObject( hbmp )
    hdc.DrawIcon( (0,0), small[0] )
    hbmp.SaveBitmapFile( hdc, f'{name}.bmp')

    bitmap = cvtColor(imread(f'{name}.bmp'), colorfunc)
    # os.remove(f'{name}.bmp')

    return bitmap
