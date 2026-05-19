include "squares_placement.dzn";
include "diffn.mzn";
include "cumulative.mzn";

int: n; 
set of int: SQUARES = 1..n;
array[SQUARES] of int: s = [i | i in SQUARES];

int: sum_sides = sum(i in SQUARES)(s[i]);
int: max_dim = sum_sides + n; 

var 0..max_dim: width;
var 0..max_dim: height;

array[SQUARES] of var 0..max_dim: x; 
array[SQUARES] of var 0..max_dim: y; 

var 0..max_dim*max_dim: obj = width * height;
solve minimize obj;

% Podstawowe ograniczenia kontenera
constraint forall(i in SQUARES) (
    x[i] + s[i] <= width /\
    y[i] + s[i] <= height
);

% Ograniczenia zapobiegające nakładaniu
constraint diffn(x, y, s, s);

% Ograniczenia skumulowane dla optymalizacji
constraint cumulative(x, s, s, height);
constraint cumulative(y, s, s, width);

% 1. Największy kwadrat przylega do lewej krawędzi (znacznie przyspiesza obliczenia)
constraint x[n] = 0;

% 2. Wymuszona proporcja kontenera
constraint width <= (3 * height) div 2;

output [
    "Optimal solution found with area: \(obj)\n",
    "Width: \(width), Height: \(height)\n",
    "Square placements (x, y):\n"
] ++
[
    "  Square \(i) (size \(s[i])): at (\(x[i]), \(y[i]))\n" | i in SQUARES
];