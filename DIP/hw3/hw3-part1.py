from tkinter import *
import tkinter
from PIL import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
import numpy
import math

window = tkinter.Tk()
window.title('DIP-HW3-B063040002-part1')
window.geometry('1200x650+40+40')
window.configure(background = 'white')

p1 = 'Fig0460a.tif'
load = Image.open(p1)
load = load.resize((373, 581), Image.BILINEAR)
load_n = load.copy()
img = ImageTk.PhotoImage(load)
img_n = img
origin = tkinter.Label(window, image = img, width = 373, height = 581)
origin.place(x = 20, y = 30)
adjust = tkinter.Label(window, image = img_n, width = 373, height = 581)
adjust.place(x = 420, y = 30)

def hit_df():
	global load
	global load_n
	global img_n
	low.set(0.4); l = 0.4
	high.set(3); h = 3
	cst.set(5); c = 5
	d0.set(20); d = 20
	data = numpy.double(numpy.array(load))
	numpy.seterr(divide = 'ignore')
	F = numpy.fft.fft2(numpy.log(data+1))
	for i in range(256):
		for j in range(256):
			e = (-c)*((pow(i-128, 2)+pow(j-128, 2))/pow(d, 2))
			p = 1-math.exp(e)
			F[i, j] = (h-l)*p+l
	L = 24*c*numpy.exp(numpy.real(numpy.fft.ifft2(F)-1))
	load_n = Image.fromarray(numpy.uint8(L))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_uf():
	global load
	global load_n
	global img_n
	l = low.get()
	h = high.get()
	c = cst.get()
	d = d0.get()
	data = numpy.double(numpy.array(load))
	numpy.seterr(divide = 'ignore')
	F = numpy.fft.fft2(numpy.log(data+1))
	for i in range(256):
		for j in range(256):
			e = (-c)*((pow(i-128, 2)+pow(j-128, 2))/pow(d, 2))
			p = 1-math.exp(e)
			F[i, j] = (h-l)*p+l
	L = 24*c*numpy.exp(numpy.real(numpy.fft.ifft2(F)-1))
	load_n = Image.fromarray(numpy.uint8(L))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def mv_low(self):
	pass

def mv_high(self):
	pass

def mv_cst(self):
	pass

def mv_d0(self):
	pass

des = tkinter.Button(window, text = 'designated\nhomomorphic filter', command = hit_df)
des.place(x = 850, y = 510)
user = tkinter.Button(window, text = 'user set\nhomomorphic filter', command = hit_uf)
user.place(x = 1013, y = 510)

adj = Frame(window, bg = 'gray', width = 300, height = 420)
adj.place(x = 850, y = 80)
low = Scale(adj, label = 'γL', bg = 'gray', length = 260, orient = HORIZONTAL, command = mv_low, from_ = 0, to = 0.8, resolution = 0.05)
low.place(x = 20, y = 30)
high = Scale(adj, label = 'γH', bg = 'gray', length = 260, orient = HORIZONTAL, command = mv_high, from_ = 2, to = 4, resolution = 0.1)
high.place(x = 20, y = 130)
cst = Scale(adj, label = 'c', bg = 'gray', length = 260, orient = HORIZONTAL, command = mv_cst, from_ = 1, to = 10, resolution = 1)
cst.place(x = 20, y = 230)
d0 = Scale(adj, label = 'D0', bg = 'gray', length = 260, orient = HORIZONTAL, command = mv_d0, from_ = 10, to = 100, resolution = 10)
d0.place(x = 20, y = 330)
low.set(0)
high.set(2)
cst.set(1)
d0.set(10)

window.mainloop()
