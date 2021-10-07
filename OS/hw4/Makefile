all: hw4

hw4: b063040002-hw4-part2.c mm.o
	gcc -o hw4 b063040002-hw4-part2.c mm.o
mm.o: mm.c
	gcc -c mm.c
dep: 
	gcc -M *.c>.depend
clean: 
	rm -f *.o hw4
