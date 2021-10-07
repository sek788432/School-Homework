#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h> 
#include<sys/mman.h> 
#include<sys/stat.h> 
#include<unistd.h> 

#define FILE_LENGTH 0x100

int main(){	
	printf("B063040002 HW5\n");
	while(1){
		int fd;	
		char temp[1000];
		char s[100];
		void* file;
		
		fd = open ("TEST",O_RDWR, S_IRUSR | S_IWUSR); 
		if(fd<0)
			printf("I am wrong.\n");
		
		file=mmap (0, FILE_LENGTH, PROT_READ, MAP_SHARED, fd, 0);
			
		//fget(s,99,stdin);
		sscanf((char*)file,"%[^\n]",s);
		printf("What in memory: %s\n",s);
		sleep(1);
				
		close(fd);
		munmap (file,FILE_LENGTH); 
	}
	return 0;
}
