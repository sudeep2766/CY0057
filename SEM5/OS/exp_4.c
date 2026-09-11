#include <stdio.h>
#include<pthread.h>

void *print_message(void *arg){
    char *message = (char *) arg;
    int i;
    for (i = 0; i<3; i++)
        printf("Thread [%s]: iteration %d\n", message, i+1);
    pthread_exit(NULL);
}

int main(){
    pthread_t t1, t2;

    pthread_create(&t1, NULL, print_message, (void *) "Thread-1");
    pthread_create(&t2, NULL, print_message, (void *) "Thread-2");

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Both threads have finished exec.\n");
    return 0;


}