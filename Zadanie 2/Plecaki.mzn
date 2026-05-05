int: items_n;            
int: knapsacks_n;       
int: capacity;          

array[1..items_n] of int: weights;  
array[1..items_n] of int: values;   

array[1..knapsacks_n, 1..items_n] of var 0..1: taken;

constraint forall(j in 1..items_n) (
  sum(i in 1..knapsacks_n)(taken[i,j]) <= 1
);

constraint forall(i in 1..knapsacks_n) (
  sum(j in 1..items_n)(weights[j] * taken[i,j]) <= capacity
);

constraint forall(i in 1..knapsacks_n-1)(
  lex_less([ taken[i,j] | j in 1..items_n ], [ taken[i+1,j] | j in 1..items_n ])
);

var int: total_value = sum(i in 1..knapsacks_n, j in 1..items_n)(values[j] * taken[i,j]);

solve maximize total_value;

output [
  "Total value = ", show(total_value), "\n"
] ++
[
  "Knapsack " ++ show(i) ++ ": " ++ show([ j | j in 1..items_n where fix(taken[i,j]) = 1 ]) ++ "\n"
  | i in 1..knapsacks_n
];