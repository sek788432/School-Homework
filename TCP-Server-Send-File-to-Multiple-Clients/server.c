#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include <ctype.h>
#include<sys/wait.h>
#define buffer_size 10240
#define IP "127.0.0.1"


int sockfd,r,newSocket,packet[2],PORT,client_port ;
struct sockaddr_in serverAddr;
struct sockaddr_in newAddr;
char fileName[20],myIP[20];
socklen_t addr_size = sizeof(newAddr);
pid_t pid,w_pid;


void connection()
{
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if(sockfd < 0){
    printf("Connection Error.\n");
    exit(1);
  }

  //Release Port
  int optval = 1;
  setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,
     (const void *)&optval , sizeof(int));


  memset(&serverAddr, 0, sizeof(serverAddr));
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(PORT);
  serverAddr.sin_addr.s_addr = inet_addr(IP);

  r = bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
  if(r < 0){
  	printf("Binding Error.\n");
  	exit(1);
  }

  if(listen(sockfd, 10) == 0){
  	printf("Listening for client....\n");
  }else{
  	printf("Binding Error.\n");
  }
}

void pass_file()
{
  FILE * fpIn = fopen(fileName, "r");
  long long  int file_size = 0;
     if (fpIn)
     {
       char buf[buffer_size];
       while(1)
       {
		 ssize_t bytesRead = fread(buf, 1, sizeof(buf), fpIn);
		 if (bytesRead <= 0) break;  // EOF
		 file_size+=(int)bytesRead;
		 if (send(newSocket, buf, bytesRead, 0) != bytesRead)
		 {
			perror("send");
			break;
		 }
       }
	  char temp[3] = {'\0','K','M'};
	  int index = 0;
	  double size = file_size;
	  while(size>=1024)
	  {
		size = size/1024.0;
		index++;
	  }
	printf("Start to send file 1 to %s : %d, the file size is %f %cB.\n",IP,client_port,size,temp[index]);

	}
	else printf("Error, couldn't open file [%s] to send!\n", fileName);
	fclose(fpIn);

}

void recieve_message()
{

  char buff[20];
  recv(newSocket, buff, sizeof(buff), 0);
  printf("Recieve a message from %s : %d\n",IP,client_port);
  printf("\tThe message is: %s\n", buff);
  strcpy(fileName, buff);
}



int main(int argc,char *argv[])
{
  PORT = atoi(argv[1]);
  connection();
  int status = 0;
	while(1){
		newSocket = accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);
		inet_ntop(AF_INET, &newAddr.sin_addr, myIP, sizeof(myIP));
		client_port = ntohs(newAddr.sin_port);
		printf("Get a connection from %s : %d\n",myIP,client_port);
		if(newSocket < 0){
			exit(1);
		}

		if((pid = fork()) == 0){
			close(sockfd);
			recieve_message();
			pass_file();
			close(newSocket);
			break;
  		}
		else if(pid > 0){
			close(newSocket);
			continue;
		}

  		//while ((w_pid = wait(&status)) > 0);  //wait until child process finish
   		//close(newSocket);
  		}

  return 0;
}
