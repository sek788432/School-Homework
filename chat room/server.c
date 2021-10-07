#include <arpa/inet.h>
#include <fcntl.h>
#include <math.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <errno.h>
#include <signal.h>
#include <time.h>

typedef struct messege
{
    char name[10][10];
    char mess[200];
    int finish;
}messege;

typedef struct pid_name
{
    pid_t pid;
    int type;
    char ip[16];
    char name[10];
}pid_name;

typedef struct pack
{
    char name[10];
    char sendto[10][10];
    char mess[200];
}pack;

typedef struct user_status
{
    char name[10];
    int offindex;
    char offlinemess[20][200];
    pid_t pid;
}user_status;

int client_fd;
messege *shmaddr;
messege *mess;
pid_name *pn;
int map_index = 10;
user_status users_map[10];

void deliverhandler(int signum)
{
    if(pn->type == 1){
        int i;
        for(i=0;i<map_index;i++)
        if (!strcmp(users_map[i].name,pn->name)) break;
        if (i == map_index){
            for(i=0; i<map_index;i++)
            if(!users_map[i].pid) break;
            strcpy(users_map[i].name,pn->name);
            users_map[i].pid = pn->pid;
        }
        else {
            users_map[i].pid = pn->pid;
            for(int j=0; j < users_map[i].offindex; j++){
                strcpy(mess->mess,users_map[i].offlinemess[j]);
                mess->finish = 0;
                kill(users_map[i].pid,SIGUSR1);
                while(!mess->finish);
            }
            users_map[i].offindex = 0;
        }
        sprintf(mess->mess,"<User %s is on-line, IP address: %s>",users_map[i].name,pn->ip);
        printf("User %s is on-line, IP address: %s",users_map[i].name,pn->ip);
        fflush(stdout);
        for(int j=0;j<map_index;j++){
            //if(j == i) continue;
            if(users_map[j].pid){
                mess->finish = 0;
                kill(users_map[j].pid,SIGUSR1);
                while(!mess->finish);
            }
        }
    }
    else if(pn->type == 2){
        int i;
        for(i=0;i<map_index;i++)
        if (!strcmp(users_map[i].name,pn->name)) break;
        users_map[i].pid = 0;
        sprintf(mess->mess,"<User %s is off-line.>",users_map[i].name);
        printf("User %s is off-line.\n",users_map[i].name);
        fflush(stdout);
        for(int j=0;j<map_index;j++)
        {
            if(j == i) continue;
            if(users_map[j].pid){
                mess->finish = 0;
                kill(users_map[j].pid,SIGUSR1);
                while(!mess->finish);
            }
        }
    }
    else if(pn->type == 3){
        printf("\nin type3\n");fflush(stdout);

        for(int i=0;i<10;i++){
            int t=0;
            if(shmaddr->name[i][0] == 0)
            break;
            for(int j=0;j<10;j++)
            if( ! strcmp(shmaddr->name[i],users_map[j].name) ){
                t = 1;
                if (users_map[j].pid){
                    printf("in handler mess = %s",shmaddr->mess);
                    strcpy(mess->mess,shmaddr->mess);
                    mess->finish = 0;
                    printf("pid = %d\n",users_map[j].pid);
                    kill(users_map[j].pid,SIGUSR1);
                    while(!mess->finish);
                }
                else {
                    sprintf(mess->mess,"<User %s is offline. The messege will be passed when he comes back.>",shmaddr->name[i]);
                    mess->finish = 0;
                    printf("offlineeeeeeeeeeee\n");fflush(stdout);
                    time_t tt;
                    time(&tt);
                    char str[100];
                    strcpy(str,ctime(&tt));
                    str[strlen(str)-1] = 0;
                    sprintf(users_map[j].offlinemess[(users_map[j].offindex)++],"<%s at %s>",shmaddr->mess,str);
                    kill(pn->pid,SIGUSR1);
                    while(!mess->finish);
                }
            }
            if(!t){
                sprintf(mess->mess,"<User %s does not exist.>",shmaddr->name[i]);
                mess->finish = 0;
                kill(pn->pid,SIGUSR1);
                while(!mess->finish);
            }
        }
    }
    memset(shmaddr, 0, sizeof(messege));
    printf("finish handler\n");
    fflush(stdout);
}

void sendtohandler(int signum)
{
    pack P;
    printf("in sendtohandler mess = %s",mess->mess);
    strcpy(P.mess,mess->mess);
    fflush(stdout);
    printf("%ld\n",write(client_fd, &P, sizeof(pack))) ;
    mess->finish = 1;
    printf("send handler finish\n");
}

int main()
{
    /*net interface*/
    struct sockaddr_in server_info, client_info;
    int addrlen = sizeof(client_info);
    static unsigned int fd;
    if ((fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) // no AF_LOCAL
    perror("creat socket error.\n");
    int enable = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int));
    char *buf = malloc(sizeof(4));
    bzero(&server_info, sizeof(server_info));

    server_info.sin_family = AF_INET;
    server_info.sin_addr.s_addr = htonl(INADDR_ANY);
    server_info.sin_port = htons(8700);

    if (bind(fd, (struct sockaddr *)&server_info, sizeof(server_info)) == -1)
    perror("bind error");
    listen(fd, 5);

    pid_t serv_pid;
    int pid_index = 0;

    int shmid = shmget(0, sizeof(messege), IPC_CREAT | 0660 );
    int shmid2 = shmget(0,sizeof(messege), IPC_CREAT | 0660 );
    int shpids = shmget(0, sizeof(pid_name), IPC_CREAT | 0660);
    shmaddr = shmat(shmid,NULL,0);
    mess = shmat(shmid2,NULL,0);
    pn = shmat(shpids,NULL,0);

    serv_pid = fork();
    if (serv_pid > 0) {
        while (1) {
            printf("server wait for login request.\n");
            if ( (client_fd = accept(fd, (struct sockaddr *)&client_info, &addrlen)) < 0)
            printf("error");
            if (!fork()) break;
            close(client_fd);
        }
    } else { // deliver messege to online users
        printf("server process prepare to deliver data to online users.\n");
        signal(SIGUSR1,deliverhandler);
        while(1){
        }
    }
    // interact with clients
    printf("hi client\n");
    signal(SIGUSR1, sendtohandler);
    pack P;
    read(client_fd, &P, sizeof(pack));
    char N[10],IP[16];
    strcpy(N,P.name);
    strcpy(IP,inet_ntoa(client_info.sin_addr));
    strcpy(pn->name, N);
    strcpy(pn->ip, IP);
    pn->type = 1;
    printf("%s %s pid = %d\n",pn->name,pn->ip,getpid());
    pn->pid = getpid();
    kill(serv_pid,SIGUSR1);
    while( read(client_fd, &P, sizeof(pack)) > 0 )
    {
        printf("receive a pack\n");
        if(!strcmp(P.name,"send")){
            for(int i=0;i<10;i++){
                printf("@%s ",P.sendto[i]);
                strcpy(shmaddr->name[i],P.sendto[i]);
            }
            fflush(stdout);
            sprintf(shmaddr->mess,"%s send you messege: %s",N,P.mess);
            pn->type = 3;
            pn->pid = getpid();
            kill(serv_pid,SIGUSR1);
        }
    }
    printf("client leave.\n");
    fflush(stdout);
    strcpy(pn->name, N);
    pn->type = 2;
    kill(serv_pid,SIGUSR1);
}
