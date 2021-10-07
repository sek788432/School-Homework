#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h> 
#include<sys/mman.h> 
#include<sys/stat.h> 
#include<unistd.h> 
#include<string.h>

#define FILE_LENGTH 0x100

int main(){	
	printf("B063040002 HW5\n");
	while(1){
		int fd;	
		char temp[100];
		char s[100];
		void* file;
		printf("Enter what you want: \n");
		//scanf("%s",&s);
		fgets(s,100,stdin);
		fd = open ("TEST", O_RDWR | O_CREAT,S_IRUSR | S_IWUSR); 
		lseek (fd, FILE_LENGTH+1, SEEK_SET); 
		write (fd, "", 1); 
		lseek (fd, 0, SEEK_SET); 
			
		if(fd<0)
			printf("Oh My God\n");
		file= mmap (0, FILE_LENGTH, PROT_WRITE, MAP_SHARED, fd, 0); 
				
		sprintf((char*)file,"%s\n",s);
			close(fd);
			printf("okay\n");
		munmap (file,FILE_LENGTH);
	}
	return 0;
}
