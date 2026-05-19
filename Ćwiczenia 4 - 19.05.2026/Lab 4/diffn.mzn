predicate diffn(array[int] of var int: x,
                array[int] of var int: y,
                array[int] of int: dx,
                array[int] of int: dy) =
    forall(i, j in index_set(x) where i < j)(
        x[i] + dx[i] <= x[j] \/
        x[j] + dx[j] <= x[i] \/
        y[i] + dy[i] <= y[j] \/
        y[j] + dy[j] <= y[i]
    );