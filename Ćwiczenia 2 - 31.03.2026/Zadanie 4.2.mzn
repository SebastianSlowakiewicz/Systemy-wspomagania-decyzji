% Długość szukanego ciągu
int: len = 5; 

% Tablica decyzyjna: ciąg o długości 'len', liczby mogą przyjmować wartości od 0 do 'len'
array[1..len] of var 0..len: magic;

% OGRANICZENIA:

% Zliczenie wystąpień dla każdej pozycji
constraint
  forall (i in 1..len) (
    % Wartość pod indeksem 'i' musi być równa liczbie wystąpień wartości 'i - 1' w całej tablicy
    magic[i] == sum(j in 1..len)(bool2int(magic[j] == i - 1))
  );

% Opcjonalne ograniczenie przyspieszające działanie solvera dla dużych 'len'
% Suma wszystkich elementów w magicznej serii zawsze równa się jej długości
constraint sum(i in 1..len)(magic[i]) == len;

% Cel: znajdź dowolny ciąg spełniający warunki
solve satisfy;

% Wyświetlenie wyniku
output [
  "Magiczna seria dla długości ", show(len), ": ", show(magic), "\n"
];