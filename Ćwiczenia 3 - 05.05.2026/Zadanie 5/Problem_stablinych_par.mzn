int: n;  

array[1..n] of string: m_names;  
array[1..n] of string: w_names;  

array[1..n, 1..n] of int: m_ranks;
array[1..n, 1..n] of int: w_ranks;

array[1..n] of var 1..n: wives;    
array[1..n] of var 1..n: husbands; 

constraint forall(m in 1..n) (husbands[wives[m]] = m);
constraint forall(w in 1..n) (wives[husbands[w]] = w);

constraint forall(m in 1..n, w in 1..n) (
    (m_ranks[m, w] < m_ranks[m, wives[m]] /\ w_ranks[w, m] < w_ranks[w, husbands[w]]) -> false
);

constraint forall(m1, m2 in 1..n where m1 != m2) (
    wives[m1] != wives[m2]  
);

constraint forall(w1, w2 in 1..n where w1 != w2) (
    husbands[w1] != husbands[w2]  
);

constraint wives[1] = 2;  

constraint wives[1] < wives[2];  

solve satisfy;

output [
    "Dopasowanie:\n" ++
    concat([ "Mężczyzna " ++ m_names[fix(m)] ++ " -> Kobieta " ++ w_names[fix(wives[m])] ++ "\n" | m in 1..n ])
]; 