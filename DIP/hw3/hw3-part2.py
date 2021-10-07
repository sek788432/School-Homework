from tkinter import *
import tkinter
from PIL import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
import numpy
import math

window = tkinter.Tk()
window.title('DIP-HW3-B063040002-part2')
window.geometry('680x650+40+40')
window.configure(background = 'white')

p2 = 'Lenna_512_color.tif'
load = Image.open(p2)
load = load.resize((300, 300), Image.BILINEAR)
load_n = load.copy()
img = ImageTk.PhotoImage(load)
img_n = img
origin = tkinter.Label(window, image = img, width = 300, height = 300)
origin.place(x = 25, y = 30)
adjust = tkinter.Label(window, image = img_n, width = 300, height = 300)
adjust.place(x = 350, y = 30)

def hit_ccok(): #show chosen RGB component image
	global load
	global load_n
	global img_n
	c = cc_chosen.get()
	op = 0
	if c == 'Red component image':
		op = 1
	elif c == 'Green component image':
		op = 2
	elif c == 'Blue component image':
		op = 3
	for i in range(300):
		for j in range(300):
			R, G, B = load.getpixel((i, j))
			if(op == 1):
				load_n.putpixel((i, j), (R, 0, 0))
			elif(op == 2):
				load_n.putpixel((i, j), (0, G, 0))
			elif(op == 3):
				load_n.putpixel((i, j), (0, 0, B))
			else:
				load_n.putpixel((i, j), (R, G, B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_hsiok(): #show chosen HSI component image
	global load
	global load_n
	global img_n
	c = hsi_chosen.get()
	op = 0
	if c == 'Hue':
		op = 1
	elif c == 'Saturation':
		op = 2
	elif c == 'Intensity':
		op = 3
	for i in range(300):
		for j in range(300):
			R, G, B = load.getpixel((i, j))
			if(op == 1):
				x = math.acos((((R-G)+(R-B))/2)/(math.sqrt(math.pow((R-G), 2)+(R-B)*(G-B))))*180/math.pi
				if B > G:
					x = int(255-(x/360)*255)
				else:
					x = int((x/360)*255)
				load_n.putpixel((i, j), (x, x, x))
			elif(op == 2):
				x = int(255*(1-(3/(R+G+B))*min(R, G, B)))
				load_n.putpixel((i, j), (x, x, x))
			elif(op == 3):
				x = int((R+B+G)/3)
				load_n.putpixel((i, j), (x, x, x))
			else:
				load_n.putpixel((i, j), (R, G, B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_undo():
	global load
	global load_n
	global img_n
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_com():
	global load
	global load_n
	global img_n
	for i in range(300):
		for j in range(300):
			R, G, B = load.getpixel((i, j))
			load_n.putpixel((i, j), (255-R, 255-G, 255-B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_sm():
	global load
	global load_n
	global img_n
	for i in range(300):
		for j in range(300):
			rp = 0; R = 0; G = 0; B = 0
			if i-2 >= 0:
				if j-2 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i-2, j-2))
					R += tR
					G += tG
					B += tB
				if j-1 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i-2, j-1))
					R += tR
					G += tG
					B += tB
				rp += 1
				tR, tG, tB = load.getpixel((i-2, j))
				R += tR
				G += tG
				B += tB
				if j+1 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i-2, j+1))
					R += tR
					G += tG
					B += tB
				if j+2 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i-2, j+2))
					R += tR
					G += tG
					B += tB
			if i-1 >= 0:
				if j-2 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i-1, j-2))
					R += tR
					G += tG
					B += tB
				if j-1 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i-1, j-1))
					R += tR
					G += tG
					B += tB
				rp += 1
				tR, tG, tB = load.getpixel((i-1, j))
				R += tR
				G += tG
				B += tB
				if j+1 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i-1, j+1))
					R += tR
					G += tG
					B += tB
				if j+2 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i-1, j+2))
					R += tR
					G += tG
					B += tB
			if i+1 < 300:
				if j-2 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i+1, j-2))
					R += tR
					G += tG
					B += tB
				if j-1 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i+1, j-1))
					R += tR
					G += tG
					B += tB
				rp += 1
				tR, tG, tB = load.getpixel((i+1, j))
				R += tR
				G += tG
				B += tB
				if j+1 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i+1, j+1))
					R += tR
					G += tG
					B += tB
				if j+2 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i+1, j+2))
					R += tR
					G += tG
					B += tB
			if i+2 < 300:
				if j-2 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i+2, j-2))
					R += tR
					G += tG
					B += tB
				if j-1 >= 0:
					rp += 1
					tR, tG, tB = load.getpixel((i+2, j-1))
					R += tR
					G += tG
					B += tB
				rp += 1
				tR, tG, tB = load.getpixel((i+2, j))
				R += tR
				G += tG
				B += tB
				if j+1 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i+2, j+1))
					R += tR
					G += tG
					B += tB
				if j+2 < 300:
					rp += 1
					tR, tG, tB = load.getpixel((i+2, j+2))
					R += tR
					G += tG
					B += tB
			if j-2 >= 0:
				rp += 1
				tR, tG, tB = load.getpixel((i, j-2))
				R += tR
				G += tG
				B += tB
			if j-1 >= 0:
				rp += 1
				tR, tG, tB = load.getpixel((i, j-1))
				R += tR
				G += tG
				B += tB
			rp += 1
			tR, tG, tB = load.getpixel((i, j))
			R += tR
			G += tG
			B += tB
			if j+1 < 300:
				rp += 1
				tR, tG, tB = load.getpixel((i, j+1))
				R += tR
				G += tG
				B += tB
			if j+2 < 300:
				rp += 1
				tR, tG, tB = load.getpixel((i, j+2))
				R += tR
				G += tG
				B += tB
			R = round(R/rp); G = round(G/rp); B = round(B/rp)
			load_n.putpixel((i, j), (R, G, B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_sh():
	global load
	global load_n
	global img_n
	for i in range(300):
		for j in range(300):
			rp = 0; R = 0; G = 0; B = 0
			if i-1 >= 0:
				rp += 1
				tR, tG, tB = load.getpixel((i-1, j))
				R += tR
				G += tG
				B += tB
			if i+1 < 300:
				rp += 1
				tR, tG, tB = load.getpixel((i+1, j))
				R += tR
				G += tG
				B += tB
			if j-1 >= 0:
				rp += 1
				tR, tG, tB = load.getpixel((i, j-1))
				R += tR
				G += tG
				B += tB
			if j+1 < 300:
				rp += 1
				tR, tG, tB = load.getpixel((i, j+1))
				R += tR
				G += tG
				B += tB
			tR, tG, tB = load.getpixel((i, j))
			R=-R; G=-G; B=-B
			R += (tR*rp)
			G += (tG*rp)
			B += (tB*rp)
			R += tR; G += tG; B += tB
			load_n.putpixel((i, j), (R, G, B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

def hit_sfok():
	global load
	global load_n
	global img_n
	load_n = load.copy()
	c = sf_chosen.get()
	op = 0
	if c == 'step1-hue':
		op = 1
	elif c == 'step2-saturation':
		op = 2
	for i in range(300):
		for j in range(300):
			R, G, B = load.getpixel((i, j))
			if(op == 1):
				if i >= 30 and i < 170 and j >= 100:
					hue = math.acos((((R-G)+(R-B))/2)/(math.sqrt(math.pow((R-G), 2)+(R-B)*(G-B))))*180/math.pi
					if B > G:
						hue = int(255-(hue/360)*255)
					else:
						hue = int((hue/360)*255)
				else:
					hue = 0
				if hue < 190 or hue > 230:
					hue = 0
				load_n.putpixel((i, j), (hue, hue, hue))
			elif(op == 2):
				if i >= 30 and i < 170 and j >= 100:
					sat = 255-int(255*(1-(3/(R+G+B))*min(R, G, B)))
				else:
					sat = 0
				if sat < 80 or sat > 240:
					sat = 0
				load_n.putpixel((i, j), (sat, sat, sat))
			else:
				if i >= 30 and i < 170 and j >= 100:
					hue = math.acos((((R-G)+(R-B))/2)/(math.sqrt(math.pow((R-G), 2)+(R-B)*(G-B))))*180/math.pi
					if B > G:
						hue = int(255-(hue/360)*255)
					else:
						hue = int((hue/360)*255)
				else:
					hue = 0
				if hue < 190 or hue > 230:
					hue = 0
				if i >= 30 and i < 170 and j >= 100:
					sat = 255-int(255*(1-(3/(R+G+B))*min(R, G, B)))
				else:
					sat = 0
				if sat < 80 or sat > 240:
					sat = 0
				if sat == 0 or hue == 0:
					R = 0; G = 0; B = 0;
				load_n.putpixel((i, j), (R,G,B))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image = img_n)

cc = Frame(window, bg = 'gray', width = 220, height = 160)
cc.place(x = 25, y = 360)
cc_g = tkinter.Label(cc, bg = 'gray', text = 'RGB component', fg = 'pink')
cc_g.place(x = 20, y = 20)
cc_option = ['Red component image', 'Green component image', 'Blue component image', 'original image']
cc_chosen = StringVar()
cc_chosen.set(cc_option[3])
cc_c = OptionMenu(cc, cc_chosen, *cc_option)
cc_c.place(x = 20, y = 60)
ccok = tkinter.Button(cc, text = 'OK', command = hit_ccok)
ccok.place(x = 160, y = 110)

hsi = Frame(window, bg = 'gray', width = 180, height = 160)
hsi.place(x = 270, y = 360)
hsi_g = tkinter.Label(hsi, bg = 'gray', text = 'HSI component', fg = 'pink')
hsi_g.place(x = 20, y = 20)
hsi_option = ['Hue', 'Saturation', 'Intensity', 'original image']
hsi_chosen = StringVar()
hsi_chosen.set(hsi_option[3])
hsi_c = OptionMenu(hsi, hsi_chosen, *hsi_option)
hsi_c.place(x = 20, y = 60)
hsiok = tkinter.Button(hsi, text = 'OK', command = hit_hsiok)
hsiok.place(x = 120, y = 110)

undo = tkinter.Button(window, text = 'original\nimage', width = 12, height = 3, command = hit_undo)
undo.place(x = 500, y = 410)

com = tkinter.Button(window, text = 'complement', command = hit_com)
com.place(x = 25, y = 560)

sm = tkinter.Button(window, text = 'smoothing', command = hit_sm)
sm.place(x = 150, y = 560)

sh = tkinter.Button(window, text = 'sharpening', command = hit_sh)
sh.place(x = 265, y = 560)

sf = Frame(window, bg = 'gray', width = 270, height = 90)
sf.place(x = 380, y = 540)
sf_g = tkinter.Label(sf, bg = 'gray', text = 'feather part', fg = 'pink')
sf_g.place(x = 20, y = 10)
sf_option = ['step1-hue', 'step2-saturation', 'final']
sf_chosen = StringVar()
sf_chosen.set(sf_option[0])
sf_c = OptionMenu(sf, sf_chosen, *sf_option)
sf_c.place(x = 20, y = 40)
sfok = tkinter.Button(sf, text = 'OK', command = hit_sfok)
sfok.place(x = 210, y = 40)

window.mainloop()
