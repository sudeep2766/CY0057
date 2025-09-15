// Online C compiler to run C program online
#include <stdio.h>

struct Student{
    int id;
    char name[50];
    char grade;
    float marks[5];
    float average;
}

void avg(struct Student *student){
    float total = 0.0;
    for (int i=0; i<5; i++){
        total += student->marks[i];
    }
    student->average = total/5;
    
}

void assignGrade(struct Student *student){
    if(student->average >= 90){
        student->grade = 'A';
    }
    else if (student->average >=80 && student->average<90){
        student->grade = 'B';
    }
    else if (student->average >=70 && student->average<80){
        student->grade = 'C';
    }
    else if (student->average >=60 && student->average<70){
        student->grade = 'D';
    }
    else if (student->average<50){
        student->grade = 'F';
    }
}
int main() {
    struct Student students[5];
    for (int i=0; i<5; i++){
        printf("Enter student ID: ");
        scanf("%d", &students[i].id);
        printf("Enter name: ");
        scanf("%s", &students[i].name);
    }
    return 0;
}
