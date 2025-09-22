#include <stdio.h>

struct Student{
    int ID;
    char name[50];
    char grade;
    float marks[5];
    float average;
};

void calcAvg(struct Student *student){
    float total = 0.0;
    for (int i=0; i<5; i++){
        total += student->marks[i];
    }
    student->average = total/5;
}

void assignGrades(struct Student *student){
    if (student->average >=90)
        student -> grade = 'A';
    else if(student->average >=80)
        student->grade = 'B';
    else if(student->average >= 70)
        student->grade = 'C';
    else if(student->average >= 60)
        student->grade = 'D';
    else
        student->grade = 'F';
}
int main() {
    struct Student students[5];
    for (int i=0; i<5; i++){
        printf("Enter student ID: ");
        scanf("%d", &students[i].ID);
        printf("Enter Name: ");
        scanf("%s", students[i].name);
        
        printf("Enter marks of 5 subjects:\n");
        for (int j=0; j<5; j++){
            printf("Subject %d: ", j+1);
            scanf("%f", &students[i].marks[j]);
        }
        calcAvg(&students[i]);
        assignGrades(&students[i]);
    }
    
    printf("\nStudent Info:\n");
    for (int i = 0; i < 5; i++){
        printf("Name: %s\t", students[i].name);
        printf("ID: %d\t", students[i].ID);
        printf("Average marks: %.2f\t", students[i].average);
        printf("Grade: %c\n", students[i].grade);
    }
    
    
    return 0;
}
