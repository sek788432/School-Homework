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
#define buffer_size 10240
char fileName[] = "client_get_";
int clientSocket,r,packet[2],PORT;
struct sockaddr_in serverAddr;
char* IP;


void connection()
{
  clientSocket = socket(AF_INET, SOCK_STREAM, 0);
  if(clientSocket<0)
  {
    printf("Connection Error.\n");
    exit(1);
  }
  int optval = 1;
  setsockopt(clientSocket, SOL_SOCKET, SO_REUSEADDR,
     (const void *)&optval , sizeof(int));

  memset(&serverAddr, 0, sizeof(serverAddr));
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(PORT);
  serverAddr.sin_addr.s_addr = inet_addr(IP);

  r = connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
  if(r < 0){
    printf("Connection Error\n");
    exit(1);
  }
}
void recv_file()
{
  FILE * fpIn = fopen(fileName, "w");
  if (fpIn)
  {
    char buf[buffer_size];
    while(1)
    {
        ssize_t bytesReceived = recv(clientSocket, buf, sizeof(buf), 0);
        if (bytesReceived < 0) perror("recv");  // network error?
        if (bytesReceived == 0) break;   // sender closed connection, must be end of file
        if (fwrite(buf, 1, bytesReceived, fpIn) != (size_t) bytesReceived)
        {
          perror("fwrite");
          break;
        }
     }
    printf("Recieve 1 file  from %s : %d\n",IP,PORT );

    }
    else printf("Error, couldn't open file [%s] to receive!\n", fileName);
    fclose(fpIn);
    close(clientSocket);
}

void send_message()
{
  char buff[20];
  printf("Input the file name you want: ");
  scanf("%s",buff);
  write(clientSocket, buff, sizeof(buff));
  strcat(fileName, buff);
  printf("%s\n",fileName);
  printf("You sent a message to %s : %d\n",IP,PORT);

}



int main(int argc, char* argv[])
{
  IP = argv[1];
  PORT = atoi(argv[2]);
  connection();
  send_message();
  recv_file();
  return 0;
}
