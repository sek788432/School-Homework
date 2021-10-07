#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>
#include<semaphore.h>

#define N 5
#define LEFT (i+N-1)%N
#define RIGHT (i+1)%N

#define THINKING 0
#define HUNGRY 1
#define EATING 2

int state[N];
sem_t waittype;
sem_t posttype[N]; //semaphore is a counter, it can be visited when it's bigger than 0
pthread_t thread[N];

void show_state(){
	printf("\t\t");
	for(int t = 0; t < N; t++){
		if(state[t]==THINKING)printf(" T ");
		else if(state[t]==HUNGRY)printf(" H ");
		else if(state[t]==EATING)printf(" E ");
	}
	printf("\n");
}

void test(int i){
	if(state[i]==HUNGRY && state[LEFT]!=EATING && state[RIGHT]!=EATING){
		state[i]=EATING;
		printf("philosopher %d is EATING  ", i+1);
		show_state();
		sem_post(&posttype[i]); //up(), increase semaphore
	}
}

void take_forks(int i){
	sem_wait(&waittype); //down()
	state[i] = HUNGRY;
	printf("philosopher %d is HUNGRY  ", i+1);
	show_state();
	test(i);
	sem_post(&waittype);
	sem_wait(&posttype[i]);
	sleep(1);
}

void put_forks(int i){
	sem_wait(&waittype);
	state[i] = 0;
	printf("philosopher %d is THINKING", i+1);
	show_state();
	test(LEFT);
	test(RIGHT);
	sem_post(&waittype);
	sleep(1);
}

void philosopher(void* n){
	int i = *(int*)n;
	while(1){
		sleep(1);
		take_forks(i);
		sleep(3);
		put_forks(i);
	}
}

int main(void){
	int p[N] = {0, 1, 2, 3, 4};
	sem_init(&waittype, 0, 1);
	printf("-----T represents THINKING, H represents HUNGRY, E represnts EATING-----\n");
	for(int t = 0; t < N; t++){
		pthread_create(&thread[t], NULL, (void*)philosopher, (void*)&p[t]);
	}
	for(int t = 0; t < N; t++){
		pthread_join(thread[t], NULL); //pause current thread until target thread finishes
	}
	return 0;
}
