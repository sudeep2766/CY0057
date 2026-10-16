#include<stdio.h>
#define MAX 100

int main(){
    int n, choice, i, j;
    int bt[MAX], at[MAX], p[MAX];
    int wt[MAX], tat[MAX], ct[MAX];
    int rem[MAX], priority[MAX];
    int time, tq, completed;

    float avgwt, avgtat;

    printf("CPU PROCESS SCHEDULING ALGORITHMS\n");
    printf("1. FCFS\n");
    printf("2. SJF (Non-preemptive)\n");
    printf("3. Priority (Non-preemptive)\n");
    printf("4. Round Robin\n");

    printf("Enter your choice: ");
    scanf("%d", &choice);

    printf("Enter number of processes: ");
    scanf("%d", &n);

    if(n < 1 || n > MAX){
        printf("Invalid number of processes!\n");
        return 1;
    }

    for(i = 0; i < n; i++){
        p[i] = i + 1;

        printf("\nProcess P%d\n", p[i]);

        printf("Enter arrival time: ");
        scanf("%d", &at[i]);

        printf("Enter burst time: ");
        scanf("%d", &bt[i]);

        printf("Enter priority: ");
        scanf("%d", &priority[i]);

        if(at[i] < 0 || bt[i] <= 0){
            printf("Invalid arrival or burst time!\n");
            return 1;
        }

        rem[i] = bt[i];
    }

    if(choice == 4){
        printf("Enter time quantum: ");
        scanf("%d", &tq);

        if(tq <= 0){
            printf("Invalid time quantum!\n");
            return 1;
        }
    }

    if(choice < 1 || choice > 4){
        printf("Invalid choice!\n");
        return 1;
    }
    
    // FCFS
    if (choice == 1){
        for(i=0; i<n; i++){
            for(j=i+1; j<n; j++){
                if(at[i] > at[j]){
                    int temp;
                    temp = at[i];
                    at[i] = at[j];
                    at[j] = temp;

                    temp = bt[i];
                    bt[i] = bt[j];
                    bt[j] = temp;

                    temp = p[i];
                    p[i] = p[j];
                    p[j] = temp;
                }
            }
        }
        time = 0;
        for(i = 0; i<n; i++){
            if(time < at[i]){
                time = at[i];
            }
            time += bt[i];
            ct[i] = time;
            tat[i] = ct[i] - at[i];
            wt[i] = tat[i] - bt[i];
        }
    }

    // SJF
    else if(choice == 2){
        time = 0;
        completed = 0;
        while (completed < n){
            int idx = -1;
            for(i=0; i<n; i++){
                if(at[i] <= time && rem[i] > 0){
                    if(idx == -1 || bt[i] < bt[idx]){
                        idx = i;
                    }
                }
            }
            if(idx == -1){
                time++;
                continue;
            }
            time += bt[idx];
            ct[idx] = time;
            tat[idx] = ct[idx] - at[idx];
            wt[idx] = tat[idx] - bt[idx];
            rem[idx] = 0;
            completed++;
        }
    }

    // Priority
    else if(choice == 3){
        time = 0;
        completed = 0;
        while (completed < n){
            int idx = -1;
            for(i=0; i<n; i++){
                if(at[i] <= time && rem[i] > 0){
                    if(idx == -1 || priority[i] < priority[idx]){
                        idx = i;
                    }
                }
            }
            if(idx == -1){
                time++;
                continue;
            }
            time += bt[idx];
            ct[idx] = time;
            tat[idx] = ct[idx] - at[idx];
            wt[idx] = tat[idx] - bt[idx];
            rem[idx] = 0;
            completed++;
        }
    }

    // Round robin
    else if(choice == 4){
        time = 0;
        completed = 0;
        while(completed < n){
            int executed = 0;
            for(i=0; i<n; i++){
                if(rem[i] > 0 && at[i] <= time){
                    executed = 1;
                    if(rem[i] > tq){
                        time += tq;
                        rem[i] -= tq;
                    }
                    else{
                        time += rem[i];
                        rem[i] = 0;
                        ct[i] = time;
                        tat[i] = ct[i] - at[i];
                        wt[i] = tat[i] - bt[i];
                        completed++;
                    }
                }
            }
            if(!executed){
                time++;
            }
        }
    }
    // Print results
    printf("\n\nPROCESS SCHEDULING RESULTS\n");
    printf("--------------------------------------------------\n");
    printf("PID\tAT\tBT\tPriority\tCT\tTAT\tWT\n");
    printf("--------------------------------------------------\n");

    avgwt = 0;
    avgtat = 0;

    for(i = 0; i < n; i++){
        printf("P%d\t%d\t%d\t%d\t\t%d\t%d\t%d\n",
               p[i], at[i], bt[i], priority[i],
               ct[i], tat[i], wt[i]);

        avgwt += wt[i];
        avgtat += tat[i];
    }

    printf("--------------------------------------------------\n");
    printf("Average Waiting Time    = %.2f\n", avgwt / n);
    printf("Average Turnaround Time = %.2f\n", avgtat / n);
}
