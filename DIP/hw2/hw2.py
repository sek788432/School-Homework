from tkinter import *
import tkinter
from PIL import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
import numpy

window = tkinter.Tk()
window.title('DIP-HW2-B063040002')
window.geometry('900x720+40+40')

name = 'lenna_gray.tif'
load = Image.open(name)
load = load.resize((300, 300), Image.BILINEAR)  # resize to fit the label size
load_n = load.copy()  # make changes on the new image to avoid changing the original one
img = ImageTk.PhotoImage(load)
img_n = img
origin = tkinter.Label(window, bg='black', image=img, width=300, height=300)
adjust = tkinter.Label(window, bg='black', anchor='nw',
                       image=img_n, width=300, height=300)


def hit_op():
	global name
	global load
	global load_n
	global img
	global img_n
	name = box.get()
	temp = Image.open(name)
	temp = temp.resize((300, 300), Image.BILINEAR)
	sm.set(0)
	sh.set(1)
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


def hit_prs():
	global load
	global load_n
	global img_n
	lw = int(lwbd.get())
	if lw < 0:
		lw = 0
	up = int(upbd.get())
	if up > 255:
		up = 255
	for i in range(300):
		for j in range(300):
			x = load.getpixel((i, j))
			if(x >= lw and x <= up):  # change selected range of gray levels into 220 and keep unselected unchange
				x = 220
			load_n.putpixel((i, j), x)
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def hit_blk():
	global load
	global load_n
	global img_n
	lw = int(lwbd.get())
	if lw < 0:
		lw = 0
	up = int(upbd.get())
	if up > 255:
		up = 255
	for i in range(300):
		for j in range(300):
			x = load.getpixel((i, j))
			if(x >= lw and x <= up):
				x = 220
			else:
				x = 0  # change unselected range of gray levels into black
			load_n.putpixel((i, j), x)
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def hit_bpok():  # show chosen bit-plane
	global load
	global load_n
	global img_n
	b = bp_chosen.get()
	if b == 'bit-plane 0':
		b = 7
	elif b == 'bit-plane 1':
		b = 6
	elif b == 'bit-plane 2':
		b = 5
	elif b == 'bit-plane 3':
		b = 4
	elif b == 'bit-plane 4':
		b = 3
	elif b == 'bit-plane 5':
		b = 2
	elif b == 'bit-plane 6':
		b = 1
	else:
		b = 0
	for i in range(300):
		for j in range(300):
			s = bin(load.getpixel((i, j)))[2:].zfill(8)
			if s[b] == '1':
				load_n.putpixel((i, j), 255)  # if the bit is 1, let it be white
			else:
				load_n.putpixel((i, j), 0)  # if the bit is 0, let it be black
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def mv_sm(self):
	global load
	global load_n
	global img_n
	# since g(the degree of smoothing) will be the size of the mask, g must be odd
	g = sm.get()*2+1
	# use median filter with g*g mask to smooth the image
	load_n = load.filter(ImageFilter.MedianFilter(g))
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def mv_sh(self):
	global load
	global load_n
	global img_n
	g = sh.get()
	if g != 1:
		for i in range(300):
			for j in range(300):
				temp = [-1]*9  # temp is mask of 1/9g[-1, -1, -1, -1, 9g-1, -1, -1, -1, -1]
				rt = 0
				# rt is the real number of outside pixels(when the center is on the edge)
				x = 0
				if i-1 >= 0 and j-1 >= 0:
					temp[0] = load.getpixel((i-1, j-1))
					rt += 1
				if j-1 >= 0:
					temp[1] = load.getpixel((i, j-1))
					rt += 1
				if j-1 >= 0 and i+1 < 300:
					temp[2] = load.getpixel((i+1, j-1))
					rt += 1
				if i-1 >= 0:
					temp[3] = load.getpixel((i-1, j))
					rt += 1
				if i+1 < 300:
					temp[4] = load.getpixel((i+1, j))
					rt += 1
				if i-1 >= 0 and j+1 < 300:
					temp[5] = load.getpixel((i-1, j+1))
					rt += 1
				if j+1 < 300:
					temp[6] = load.getpixel((i, j+1))
					rt += 1
				if i+1 < 300 and j+1 < 300:
					temp[7] = load.getpixel((i+1, j+1))
					rt += 1
				temp[8] = load.getpixel((i, j))
				rt += 1
				for t in range(9):
					if temp[t] != -1:
						x -= temp[t]
				x += (temp[8]*g*rt)
				x /= (g*rt)
				x += temp[8]
				if x > 255:
					x = 255
				elif x < 0:
					x = 0
				load_n.putpixel((i, j), int(x))
	else:
		for i in range(300):
			for j in range(300):
				x = load.getpixel((i, j))
				load_n.putpixel((i, j), x)
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def hit_ft():
	global load_n
	global img_n
	data = numpy.array(load_n)  # make PIL image turn to numpy array
	numpy.seterr(divide='ignore')
	done = 10*numpy.log(numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(data))))
	#order: 2D FFT -> shift to center -> take absolute value(sqrt(real*real + imag*imag)) -> take log(make image visible)
	load_f = Image.fromarray(numpy.uint8(done))  # make numpy array turn to image
	img_n = ImageTk.PhotoImage(load_f)
	adjust.config(image=img_n)


def hit_nft():
	global load_n
	global img_n
	img_n = ImageTk.PhotoImage(load_n)
	adjust.config(image=img_n)


def hit_amimg():
	global load_n
	global img_n
	data = numpy.array(load_n)
	numpy.seterr(divide='ignore')
	amplitude = numpy.abs(numpy.fft.ifft2(numpy.fft.ifftshift(
		numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(data))))))
	#order: 2D FFT -> sfift to center -> take absolute value(amplitude of origin image) -> inverse shift -> inverse 2D FFT -> take absolute value
	amplitude = 10*numpy.log(amplitude)
	load_a = Image.fromarray(numpy.uint8(amplitude))
	img_n = ImageTk.PhotoImage(load_a)
	adjust.config(image=img_n)


def hit_phimg():
	global load_n
	global img_n
	data = numpy.array(load_n)
	numpy.seterr(divide='ignore')
	phase = numpy.abs(numpy.fft.ifft2(numpy.fft.ifftshift(
		numpy.angle(numpy.fft.fftshift(numpy.fft.fft2(data))))))
	#order: 2D FFT -> sfift to center -> take angle value(phase of origin image) -> inverse shift -> inverse 2D FFT -> take absolute value
	phase = 20*numpy.log(phase)
	load_p = Image.fromarray(numpy.uint8(phase))
	img_n = ImageTk.PhotoImage(load_p)
	adjust.config(image=img_n)


def hit_inv():
	global load_n
	global img_n
	data = numpy.array(load_n)
	numpy.seterr(divide='ignore')
	amplitude = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(data)))
	phase = numpy.angle(numpy.fft.fftshift(numpy.fft.fft2(data)))
	ori_real = amplitude*numpy.cos(phase)
	ori_imag = amplitude*numpy.sin(phase)
	inv = numpy.zeros((300, 300), complex)
	inv.real = numpy.array(ori_real)
	inv.imag = numpy.array(ori_imag)
	inv = numpy.abs(numpy.fft.ifft2(numpy.fft.ifftshift(inv)))
	load_i = Image.fromarray(numpy.uint8(inv))
	img_n = ImageTk.PhotoImage(load_i)
	adjust.config(image=img_n)


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

slc = Frame(window, bg='white', width=700, height=70)
slc.pack()
slc.place(x=100, y=350)
slc_g = tkinter.Label(slc, bg='white', text='gray-level\nslicing', fg='blue')
slc_g.pack()
slc_g.place(x=25, y=15)
lwbd_g = tkinter.Label(slc, bg='white', text='lower bound')
lwbd_g.pack()
lwbd_g.place(x=140, y=10)
lwbd = tkinter.Entry(slc, width=15)
lwbd.pack()
lwbd.place(x=140, y=30)
upbd_g = tkinter.Label(slc, bg='white', text='upper bound')
upbd_g.pack()
upbd_g.place(x=290, y=10)
upbd = tkinter.Entry(slc, width=15)
upbd.pack()
upbd.place(x=290, y=30)

prs = tkinter.Button(slc, text='preserve\norigin value', command=hit_prs)
prs.pack()
prs.place(x=480, y=10)
blk = tkinter.Button(slc, text='turn\nblack', command=hit_blk)
blk.pack()
blk.place(x=600, y=10)

bp = Frame(window, bg='white', width=160, height=160)
bp.pack()
bp.place(x=100, y=440)
bp_g = tkinter.Label(bp, bg='white', text='bit-plane', fg='blue')
bp_g.pack()
bp_g.place(x=25, y=15)
bp_option = ['bit-plane 0', 'bit-plane 1', 'bit-plane 2', 'bit-plane 3',
             'bit-plane 4', 'bit-plane 5', 'bit-plane 6', 'bit-plane 7']
bp_chosen = StringVar()
bp_chosen.set(bp_option[0])
bp_c = OptionMenu(bp, bp_chosen, *bp_option)
bp_c.pack()
bp_c.place(x=25, y=60)
bpok = tkinter.Button(bp, text='OK', command=hit_bpok)
bpok.pack()
bpok.place(x=90, y=120)

flt = Frame(window, bg='white', width=520, height=160)
flt.pack()
flt.place(x=280, y=440)
sm = Scale(flt, label='smoothing', bg='white', length=480,
           orient=HORIZONTAL, command=mv_sm, from_=0, to=5, resolution=1)
sm.pack()
sm.place(x=20, y=10)
sm.set(0)
sh = Scale(flt, label='sharpening', bg='white', length=480,
           orient=HORIZONTAL, command=mv_sh, from_=1, to=1.5, resolution=0.02)
sh.pack()
sh.place(x=20, y=90)
sh.set(1)

ft = tkinter.Button(window, text='FFT', height=3, width=5, command=hit_ft)
ft.pack()
ft.place(x=105, y=620)

nft = tkinter.Button(window, text='UNFFT', height=3, width=5, command=hit_nft)
nft.pack()
nft.place(x=185, y=620)

amimg = tkinter.Button(window, text='amplitude\nimage',
                       height=3, width=8, command=hit_amimg)
amimg.pack()
amimg.place(x=470, y=620)

phimg = tkinter.Button(window, text='phase\nimage',
                       height=3, width=8, command=hit_phimg)
phimg.pack()
phimg.place(x=570, y=620)

inv = tkinter.Button(window, text='amplitude image\n+\nphase image',
                     height=3, width=14, command=hit_inv)
inv.pack()
inv.place(x=670, y=620)

window.mainloop()
