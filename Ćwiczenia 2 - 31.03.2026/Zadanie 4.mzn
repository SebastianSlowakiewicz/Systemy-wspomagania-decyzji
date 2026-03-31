%Zadanie 4

int: len = 4;  

array[1..len] of var 0..len: series;

constraint
    forall(i in 1..len) (
        count(series, i-1) == series[i]
    );

solve satisfy;

output [ show(series) ];