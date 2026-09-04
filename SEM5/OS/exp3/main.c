#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>

#define BUF_SIZE 1024

int  main(){
    int src_fd, dest_fd;
    ssize_t bytes_read;
    char buffer[BUF_SIZE];
    char source[100], destination[100];

    printf("Enter source file name: ");
    scanf("%99s", source);

    printf("Enter the destination file name: ");
    scanf("%99s", destination);

    src_fd = open(source, O_RDONLY);
    if(src_fd == -1){
        perror("Error opening source file");
        exit(1);
    }
    dest_fd = open(destination, O_WRONLY | O_CREAT | O_TRUNC, 0644);

    if(dest_fd == -1){
        perror("Error opening the destination file");
        close(src_fd);
        exit(1);
    }

    while((bytes_read = read(src_fd, buffer, BUF_SIZE)) > 0){
        if(write(dest_fd, buffer, bytes_read) != bytes_read){
            perror("Error writing to destination file");
            close(src_fd);
            close(dest_fd);
            exit(1);
        }
    }
    if(bytes_read == -1){
        perror("Error reading the source");
        close(src_fd);
        close(dest_fd);
        exit(1);
    }
    printf("File copied successfully");
    close(src_fd);
    close(dest_fd);
}
