#include<stdio.h>
#include<stdlib.h>

struct Node{
    int data;
    struct Node* next;
};

struct Node* insertAtBeginning(struct Node* head, int value){
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if(newNode == NULL){
        printf("Memory allocation failed!\n");
        return head;
    }

    newNode->data = value;
    newNode->next = head;
    return newNode;
}

struct Node* insertAtEnd(struct Node* head, int value){
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;
    if(head == NULL){
        return newNode;
    }
    struct Node* last = head;
    while(last->next != NULL){
        last = last->next;
    }
    last->next = newNode;
    return head;
}

struct Node* removeByValue(struct Node* head, int value){
    

    struct Node *current = head;
    while(current->data != NULL || current->data != value){
        current = current->next;
    }
}
