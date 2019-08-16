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