int: n = 120;  

array[0..n-1] of var 0..n-1: magic;

constraint 
  forall(i in 0..n-1) (
      magic[i] = sum(j in 0..n-1)(bool2int(magic[j] = i))
  );

constraint sum(magic) = n;

constraint sum(i in 0..n-1)(magic[i] * i) = n;

solve satisfy;

output ["magic = ", show(magic)];