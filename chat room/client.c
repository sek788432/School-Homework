#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <signal.h>
#include <unistd.h>
typedef struct pack
{
    char name[10];
    char sendto[10][10];
    char mess[200];
}pack;

int main()
{
    struct sockaddr_in info;
    unsigned int fd;
    if ((fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // no AF_LOCAL
    perror("creat socket error.\n");

    bzero(&info, sizeof(info));
    while (1) {
        printf("$ ");
        char tmp[20];
        pid_t pid;
        scanf("%s", tmp);
        if (!strcmp(tmp, "bye")) {
            kill(pid,SIGINT);
            printf("See you next time.\n");
            exit(1);
        } else if (!strcmp(tmp, "connect")) {
            char ip[100], port[100];
            char name[10];
            scanf(" %s %s %s", ip, port, name);
            info.sin_family = AF_INET;
            info.sin_addr.s_addr = inet_addr(ip);
            info.sin_port = htons(atoi(port));
            if (connect(fd, (struct sockaddr *)&info, sizeof(info)) == -1)
            perror("connect error");
            else{
                printf("The server with IP “%s” has accepted your connection. \n", ip);
                pack buf;
                strcpy(buf.name,name);
                write(fd , &buf, sizeof(buf));
                if((pid = fork()) == 0) break;
            }
        } else if (!strcmp(tmp, "chat")) {
            pack P;
            memset(&P,0,sizeof(P));
            char command[200];
            scanf(" %s",command);
            int i=0;
            while(command[0] != '\"'){
                strcpy(P.sendto[i++],command);
                scanf("%s",command);
            }
            strcpy(P.name,"send");
            strcpy(P.mess,command);
            write(fd ,&P, sizeof(P));
        }
    }
    //interface with server
    pack P;
    int s;
    while((s = recv(fd,&P,sizeof(pack), MSG_WAITALL)) > 0 ){
        printf("%s\n",P.mess);
        printf("$ ");
        fflush(stdout);
    }

}
