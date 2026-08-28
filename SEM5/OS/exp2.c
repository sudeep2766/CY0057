// PID and PPID Exp2
#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>

int main(){
    pid_t pid = fork();
    if (pid < 0){
        perror("Fork failed!");
        return 1;
    }
    else if(pid == 0){
        printf("Child process -> PID: %d, PPID: %d\n", getpid(), getppid());
    }
    else{
        wait(NULL);
        printf("Parent process -> PID: %d, PPID: %d\n", getpid(), getppid());
    }
    return 0;
}
