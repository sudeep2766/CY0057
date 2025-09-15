#include <stdio.h>

int isValid(int arr[9][9]){
    int row[9][9] = {0};
    int col[9][9] = {0};
    int box[9][9] = {0};
    
    for (int i=0; i<9; i++){
        for (int j=0; j<9; j++){
            
        }
    }
}
int main() {
    int board[SIZE][SIZE] = {
        {5, 3, 0, 0, 7, 0, 0, 0, 0},
        {6, 0, 0, 1, 9, 5, 0, 0, 0},
        {0, 9, 8, 0, 0, 0, 0, 6, 0},
        {8, 0, 0, 0, 6, 0, 0, 0, 3},
        {4, 0, 0, 8, 0, 3, 0, 0, 1},
        {7, 0, 0, 0, 2, 0, 0, 0, 6},
        {0, 6, 0, 0, 0, 0, 2, 8, 0},
        {0, 0, 0, 4, 1, 9, 0, 0, 5},
        {0, 0, 0, 0, 8, 0, 0, 7, 9}
    };
    
    if (isValid(board))
        printf("Valid Sudoku\n");
    else
        printf("Invalid!\n");
    return 0;
}
