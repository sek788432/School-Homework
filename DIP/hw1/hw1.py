from tkinter import *
import tkinter
from PIL import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageOps
import matplotlib.pyplot as plt
import math

window = tkinter.Tk()
window.title('Image Process Tool')
window.geometry('900x720+40+40')  # width = 800, height = 720

name = 'LennaGray256.tif'
load = Image.open(name)
load = load.resize((300, 300), Image.BILINEAR)  # resize to fit the label size
load_n = load.copy()  # make changes on the new image to avoid changing the original one
img = ImageTk.PhotoImage(load)
img_n = img
origin = tkinter.Label(window, bg='black', image=img, width=300, height=300)
adjust = tkinter.Label(window, bg='black', anchor='nw',
                       image=img_n, width=300, height=300)

md_c = 0  # click botton md to change method(controlled by md_c)


def hit_op():
	global name
	global load
	global load_n
	global img
	global img_n
	global md_c
	md_c = 0
	md.config(text='method')
	a.set(1)
	b.set(0)
	zm.set(0)
	name = box.get()
	temp = Image.open(name)
	temp = temp.resize((300, 300), Image.BILINEAR)
	load = temp.copy()
	load_n = load.copy()
	img = ImageTk.PhotoImage(load)
	img_n = img
	origin.config(image=img)
	adjust.config(image=img_n)
	origin.pack()
	origin.place(x=200, y=25)
	adjust.pack()
	adjust.place(x=550, y=25)


def hit_sv():
	global load_n
	load_n.save('new_' + name)  # save the changed image


def hit_md():
	global md_c
	a.set(1)  # reset scale a to 1
	b.set(0)
	if md_c == 1:
		md.config(text='exponentially')
		md_c = 2
	elif md_c == 2:
		md.config(text='logarithmically')
		md_c = 3
	else:
		md.config(text='linearly')
		md_c = 1


def mv_a(self):
	global md_c
	global load
	global load_n
	global img
	global img_n
	h, w = load_n.size
	if h > 300:
		h = 300
	if w > 300:
		w = 300
	if md_c == 1:
		for i in range(h):
			for j in range(w):
				x = load.getpixel((i, j))  # get gray level from the original image
				if (x * a.get() + b.get()) >= 255:
					x = 255
				else:
					x = x * a.get() + b.get()
				load_n.putpixel((i, j), int(x))  # put adjusted gray level to the new image
	elif md_c == 2:
		if a.get() == 1:  # reset
			for i in range(h):
				for j in range(w):
					x = load.getpixel((i, j))
					load_n.putpixel((i, j), int(x))
		else:
			for i in range(h):
				for j in range(w):
					x = load.getpixel((i, j))
					if (math.exp(x * (a.get() + 0.8) * 0.02)) >= 255:
						x = 255
					else:
						x = math.exp(x * (a.get() + 0.8) * 0.02)
					load_n.putpixel((i, j), int(x))
	elif md_c == 3:
		if a.get() == 1:
			for i in range(h):
				for j in range(w):
					x = load.getpixel((i, j))
					load_n.putpixel((i, j), int(x))
		else:
			for i in range(h):
				for j in range(w):
					x = load.getpixel((i, j))
					if (math.log1p(x * pow(10, a.get() * 10))) >= 255:
						x = 255
					else:
						x = math.log1p(x * pow(10, a.get() * 10))
					load_n.putpixel((i, j), int(x))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def mv_b(self):
	global md_c
	global load
	global load_n
	global img
	global img_n
	h, w = load_n.size
	if h > 300:
		h = 300
	if w > 300:
		w = 300
	if md_c == 1:
		for i in range(h):
			for j in range(w):
				x = load.getpixel((i, j))
				if (x * a.get() + b.get()) >= 255:
					x = 255
				else:
					x = x * a.get() + b.get()
				load_n.putpixel((i, j), int(x))
	elif md_c == 2:
		for i in range(h):
			for j in range(w):
				x = load.getpixel((i, j))
				if (math.exp(x * (a.get() + 0.8) * 0.02 + (b.get() * 0.01))) >= 255:
					x = 255
				else:
					x = math.exp(x * (a.get() + 0.8) * 0.02 + (b.get() * 0.01))
				load_n.putpixel((i, j), int(x))
	elif md_c == 3:
		if b.get() > 1:
			for i in range(h):
				for j in range(w):
					x = load.getpixel((i, j))
					if (math.log1p(x * pow(10, a.get() * 10) + pow(10, b.get()))) >= 255:
						x = 255
					else:
						x = math.log1p(x * pow(10, a.get() * 10) + pow(10, b.get()))
					load_n.putpixel((i, j), int(x))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def mv_zm(self):
	global load_n
	global img_n
	k = 300 * pow(10, zm.get())
	load_s = load_n.resize((int(k), int(k)), Image.BILINEAR)
	img_n = ImageTk.PhotoImage(load_s)
	adjust.config(image=img_n)


def hit_hg():
	global load_n
	global img_n
	show = Toplevel()  # new window
	show.title('equalization')
	show.geometry('360x360+80+80')
	load_e = ImageOps.equalize(load_n)
	img_e = ImageTk.PhotoImage(load_e)
	eq = tkinter.Label(show, image=img_e, width=300, height=300)
	eq.pack()
	eq.place(x=30, y=30)
	hist1 = load_n.histogram()
	hist2 = load_e.histogram()
	for i in range(0, 256):
		# before equalization shows red
		plt.bar(i, hist1[i], color='red', edgecolor='white')
		# after equalization shows blue
		plt.bar(i, hist2[i], color='blue', edgecolor='white')
	plt.show()
	show.mainloop()


guide = tkinter.Label(window, text='Enter the file name')
guide.pack()
guide.place(x=20, y=20)
box = tkinter.Entry(window, bd=3)
box.pack()
box.place(x=20, y=40)

op = tkinter.Button(window, text='open', command=hit_op)
op.pack()
op.place(x=110, y=80)
sv = tkinter.Button(window, text='save', command=hit_sv)
sv.pack()
sv.place(x=110, y=120)

br = Frame(window, bg='white', width=700, height=200)
br.pack()
br.place(x=100, y=350)
md = tkinter.Button(br, width=12, text='method', command=hit_md)
md.pack()
md.place(x=20, y=80)
a = Scale(br, label='a', length=500, orient=HORIZONTAL,
          command=mv_a, from_=0, to=3, resolution=0.2)
a.pack()
a.place(x=170, y=20)
a.set(1)
b = Scale(br, label='b', length=500, orient=HORIZONTAL,
          command=mv_b, from_=-10, to=10, resolution=1)
b.pack()
b.place(x=170, y=120)
b.set(0)

zm_l = tkinter.Label(window, text='zoom')
zm_l.pack()
zm_l.place(x=150, y=580)
zm = Scale(window, length=500, orient=HORIZONTAL,
           command=mv_zm, from_=-1, to=1, resolution=0.1)
zm.pack()
zm.place(x=230, y=560)
zm.set(0)

hg = tkinter.Button(window, text='histogram', command=hit_hg)
hg.pack()
hg.place(x=125, y=635)

window.mainloop()
