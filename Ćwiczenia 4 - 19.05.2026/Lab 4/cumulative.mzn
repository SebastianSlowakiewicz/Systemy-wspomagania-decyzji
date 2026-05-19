predicate cumulative(array[int] of var int: s,  % start times
                     array[int] of int: d,      % durations
                     array[int] of int: r,      % resource use
                     var int: b) =              % resource bound 
    forall(t in lb_array(s)..ub_array(s) + max(d)) (
        sum(i in index_set(s)) (
            bool2int(s[i] <= t /\ t < s[i] + d[i]) * r[i]
        ) <= b
    );