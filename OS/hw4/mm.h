#ifndef MM_H
#define MM_H
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

typedef struct mem_control_block{
	int available;
	int size;
} mcb;

void* mymalloc(size_t size);
void* mycalloc(size_t nmemb, size_t size);
void* myrealloc(void *ptr, size_t size);
void myfree(void *ptr);

void *start;
void *last;
void initial();
int has_initial;

#endif
