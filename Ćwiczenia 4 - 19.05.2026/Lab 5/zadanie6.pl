delta(A, B, C, Delta) :-
    Delta is B*B - 4*A*C.


kwadrat(A, B, C, Rozwiazania) :-
    delta(A, B, C, D),
    (
        D < 0 ->
            Rozwiazania = [] ;
        D =:= 0 ->
            X is -B / (2*A),
            Rozwiazania = [X] ;
        D > 0 ->
            SqrtD is sqrt(D),
            X1 is (-B + SqrtD) / (2*A),
            X2 is (-B - SqrtD) / (2*A),
            Rozwiazania = [X1, X2]
    ).