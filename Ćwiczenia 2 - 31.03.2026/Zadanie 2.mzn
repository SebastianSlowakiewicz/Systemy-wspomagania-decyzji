% Zadanie 2: Kolorowanie wierzchołków grafu

int: n = 5; % liczba wierzchołków
int: m = 6; % liczba krawędzi

% Tablica dwuwymiarowa przechowująca pary połączonych wierzchołków
array[1..m, 1..2] of int: edges = 
[| 1, 2
 | 1, 5
 | 2, 3
 | 3, 4
 | 4, 5
 | 5, 3 |];
 
% Zmienna przechowująca maksymalny użyty kolor (chcemy ją zminimalizować)
var 1..n: colorsNumber;

% Tablica decyzyjna: przypisuje każdemu wierzchołkowi (od 1 do n) jakiś kolor (od 1 do n)
array[1..n] of var 1..n: nodes;

% Ograniczenie 1: Liczba użytych kolorów to najwyższy numer koloru w tablicy 'nodes'
constraint colorsNumber = max(nodes);

% Ograniczenie 2: Główne zadanie.
% Dla każdej krawędzi z tablicy 'edges', jej początek i koniec muszą mieć inny kolor.
constraint
  forall(e in 1..m) (
    nodes[edges[e, 1]] != nodes[edges[e, 2]]
  );

% Cel: Znajdź rozwiązanie, które używa najmniejszej możliwej liczby kolorów
solve minimize colorsNumber;

% Wyświetlenie wyników w czytelnej formie
output [
  "Liczba kolorów: ", show(colorsNumber), "\n",
  "Przypisane kolory (wierzchołki 1 do 5): ", show(nodes)
];