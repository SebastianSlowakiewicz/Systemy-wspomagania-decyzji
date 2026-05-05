int: nodesNumber;
int: minColorsNumber;
array [1..nodesNumber, 1..nodesNumber] of bool: edges;

array[int] of int: maxClique;

array[1..nodesNumber] of var 1..nodesNumber: nodes;

var 1..nodesNumber: colorsNumber = max(nodes);


constraint forall(i in 1..minColorsNumber)( nodes[i] = i );


constraint 
  forall(i, j in 1..nodesNumber where i < j)(
    if edges[i,j] then 
      nodes[i] != nodes[j]
    else 
      true
    endif
  );


solve minimize colorsNumber;

output [
  "colorsNumber = ", show(colorsNumber), "\n",
  "nodes = ", show(nodes)
];