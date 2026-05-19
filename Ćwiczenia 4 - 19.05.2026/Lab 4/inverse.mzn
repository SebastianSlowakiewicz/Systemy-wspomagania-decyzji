predicate inverse(array[int] of var int: f, array[int] of var int: g) =
    let {
        int: n = length(f)
    } in
    forall(i in 1..n)(g[f[i]] = i) /\
    forall(j in 1..n)(f[g[j]] = j);