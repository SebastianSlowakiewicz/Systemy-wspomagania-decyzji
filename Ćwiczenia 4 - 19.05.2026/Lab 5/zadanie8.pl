% Definicja dostepnych kolor�w
kolor(czerwony).
kolor(zielony).
kolor(niebieski).

% koloruj(P1, P2, P3, P4, P5)
% Znajduje poprawne pokolorowanie dla 5 panstw P1..P5
% przy uzyciu 3 kolor�w, zgodnie z przyjeta mapa sasiedztwa.

koloruj(P1, P2, P3, P4, P5) :-
    % Krok 1: Przypisz kolory do panstw
    kolor(P1),
    kolor(P2),
    kolor(P3),
    kolor(P4),
    kolor(P5),

    % Krok 2: Sprawdz warunki sasiedztwa (zgodnie z zalozeniami powyzej)
    % Uzywamy operatora \= (r�zne od)
    P1 \= P2,
    P1 \= P3,

    P2 \= P3,
    P2 \= P4,

    P3 \= P4,
    P3 \= P5,

    P4 \= P5.
