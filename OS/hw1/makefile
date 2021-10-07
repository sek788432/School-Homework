all: hw1

hw1: b063040002-hw1-part2.o
	gcc -o hw1 b063040002-hw1-part2.o

b063040002-hw1-part2.o: b063040002-hw1-part2.c
	gcc -c b063040002-hw1-part2.c


dep:
	gcc -M *.c > .depend

clean:
	rm -f *.o hw1 .depend
