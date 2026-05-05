include "alldifferent.mzn";

% Parametry początkowe
int: n = 3;
int: n2 = n * n;

% Tablica decyzyjna (szachownica n x n) z wartościami od 1 do n^2
array[1..n, 1..n] of var 1..n2: square;

% Obliczanie magicznej sumy (używamy 'div' do całkowitoliczbowego dzielenia)
int: magic_sum = (n * (n2 + 1)) div 2;

% OGRANICZENIA:

% 1. Wszystkie liczby w kwadracie muszą być unikalne
constraint alldifferent([square[i, j] | i, j in 1..n]);

% 2. Suma w każdym wierszu musi równać się magic_sum
constraint forall(i in 1..n) (
    sum(j in 1..n)(square[i, j]) == magic_sum
);

% 3. Suma w każdej kolumnie musi równać się magic_sum
constraint forall(j in 1..n) (
    sum(i in 1..n)(square[i, j]) == magic_sum
);

% 4. Suma na głównej przekątnej (lewy-górny do prawy-dolny)
constraint sum(i in 1..n)(square[i, i]) == magic_sum;

% 5. Suma na drugiej przekątnej (prawy-górny do lewy-dolny)
constraint sum(i in 1..n)(square[i, n - i + 1]) == magic_sum;

% Cel: znajdź dowolne ułożenie spełniające warunki
solve satisfy;

% Wyświetlenie wyniku w formie siatki
output [
   show(square[i,j]) ++ if j == n then "\n" else " " endif 
   | i, j in 1..n
];
