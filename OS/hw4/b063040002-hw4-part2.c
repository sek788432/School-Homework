#include"mm.h"

int main(void){
	int opt, len;
	int *n = NULL;

	while(1){
		printf("enter 1 to test mymalloc, 2 to test mycalloc, 3 to test myrealloc, and 4 to exit\n");
		scanf("%d", &opt);
		if(opt == 1){
			if(n != NULL){
				printf("address of previous array:%p\n", n);
				printf("elements in previous array:");
				for(int i = 0; i < len; i++)printf("%d ", n[i]);
				printf("\n");
				myfree(n);
				printf("previous array has been removed\n\n");
			}
			printf("size of new array:");
			scanf("%d", &len);
			n = (int*)mymalloc(sizeof(int) * len);
			printf("enter 1 to set elements, 2 to not\n");
			scanf("%d", &opt);
			if(opt == 1){
				for(int i = 0; i < len; i++){
					printf("n[%d]=", i);
					scanf("%d", &n[i]);
				}
			}
			printf("address of new array:%p\n", n);
			printf("elements in new array:");
			for(int i = 0; i < len; i++)printf("%d ", n[i]);
			printf("\n\n");
		}
		else if(opt == 2){
			if(n != NULL){
				printf("address of previous array:%p\n", n);
				printf("elements in previous array:");
				for(int i = 0; i < len; i++)printf("%d ", n[i]);
				printf("\n");
				myfree(n);
				printf("previous array has been removed\n\n");
			}
			printf("size of new array:");
			scanf("%d", &len);
			n = (int*)mycalloc(len, sizeof(int));
			printf("enter 1 to set elements, 2 to not\n");
			scanf("%d", &opt);
			if(opt == 1){
				for(int i = 0; i < len; i++){
					printf("n[%d]=", i);
					scanf("%d", &n[i]);
				}
			}
			printf("address of new array:%p\n", n);
			printf("elements in new array:");
			for(int i = 0; i < len; i++)printf("%d ", n[i]);
			printf("\n\n");
		}
		else if(opt == 3){
			if(n == NULL)printf("array doesn't exist\n\n");
			else{
				printf("address of previous array:%p\n", n);
				printf("elements in previous array:");
				for(int i = 0; i < len; i++)printf("%d ", n[i]);
				printf("\n\n");
				printf("size of new array:");
				scanf("%d", &len);
				n = (int*)myrealloc(n, sizeof(int) * len);
				printf("enter 1 to set elements, 2 to not\n");
				scanf("%d", &opt);
				if(opt == 1){
					for(int i = 0; i < len; i++){
						printf("n[%d]=", i);
						scanf("%d", &n[i]);
					}
				}
				printf("address of new array:%p\n", n);
				printf("elements in new array:");
				for(int i = 0; i < len; i++)printf("%d ", n[i]);
				printf("\n\n");
			}
		}
		else if(opt == 4){
			if(n != NULL)myfree(n);
			break;
		}
	}
}
