all: rr  ww

rr: hw5_r.o
	gcc -o rr hw5_r.o
hw5_r.o:hw5_r.c
	gcc -c hw5_r.c
ww: hw5_w.o
	gcc -o ww hw5_w.o
hw5_w.o:hw5_w.c
	gcc -c hw5_w.c
dep:
	gcc -M *.c > .depend
clean:
	rm -f *.o rr ww .depend
