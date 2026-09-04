#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/wait.h>

void main(){
    int pid;
    pid = fork();
    if (pid < 0){
        printf("Fork failed");
        exit(1);
    }
    else if(pid ==0){
        printf("\nNow in child process and outpput is ");
        execlp("ls", "ls", NULL);
        exit(0);
    }
    else{
        printf("Child process created successfully");
        printf("\n\tProcess id is %d\n", getpid());
        wait(NULL);
        printf("Return back to parent process now ready to exit");
        exit(0);
    }

}