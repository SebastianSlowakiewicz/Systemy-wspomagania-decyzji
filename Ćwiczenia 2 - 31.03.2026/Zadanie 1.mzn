% Zadanie 1
int: N = 8;
array[1..N] of var 1..N: queens;

constraint 
  forall(i, j in 1..N where i < j) (
    queens[i] != queens[j] /\
    abs(queens[i] - queens[j]) != abs(i - j)
  );

solve satisfy;

output [ 
  if fix(queens[i]) == j then "H " else ". " endif ++ (if j == N then "\n" else "" endif) 
  | i in 1..N, j in 1..N
];

