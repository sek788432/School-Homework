#ifndef MM_C
#define MM_C
#include"mm.h"

void initial(){
	start = (void*)(intptr_t)sbrk(0); //sbrk(0) call the program break -> heap
	last = start;
	has_initial = 1;
}

void* mymalloc(size_t size){
	if(has_initial == 0)initial();
	void *cur = start;
	void *fin = NULL;
	int n = size;
	n += sizeof(mcb);

	while(cur != last){
		mcb *pcur = cur;
		if(pcur->available == 1 && pcur->size >= n){
			pcur->available = 0;
			fin = cur; break;
		}
		cur += pcur->size;
	}
	if(fin == NULL){
		sbrk(n);
		fin = last;
		last += n;
		mcb *p = fin;
		p->size = n;
		p->available = 0;
	}
	fin += sizeof(mcb);
	return fin;
}

void* mycalloc(size_t nmemb, size_t size){
	void *temp = mymalloc(nmemb * size);
	memset(temp, 0, nmemb * size);
	return temp;
}

void* myrealloc(void *ptr, size_t size){
	void *temp = mymalloc(size);
	memcpy(temp, ptr, size);
	myfree(ptr);
	return temp;
}

void myfree(void *ptr){
	mcb *pmcb = (mcb*)(ptr - sizeof(mcb));
	pmcb->available = 1;
}

#endif
