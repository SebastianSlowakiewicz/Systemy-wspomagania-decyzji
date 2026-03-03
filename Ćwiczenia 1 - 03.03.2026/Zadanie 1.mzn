% Zadanie 1 
int: owoce = 215;
int: frytki = 275;
int: salatka = 335;
int: skrzydelka = 355;
int: paluszki = 420;
int: zestaw_probny = 580;

% Suma docelowa
int: suma = 1505;

var 0..10: x_owoce;
var 0..10: x_frytki;
var 0..10: x_salatka;
var 0..10: x_skrzydelka;
var 0..10: x_paluszki;
var 0..10: x_zestaw_probny;

constraint
    owoce * x_owoce + frytki * x_frytki + salatka * x_salatka + skrzydelka * x_skrzydelka + paluszki * x_paluszki + zestaw_probny * x_zestaw_probny == suma;

solve satisfy;

output [
  "Owoce: \(x_owoce)\n",
  "Frytki: \(x_frytki)\n",
  "Sałatka: \(x_salatka)\n",
  "Skrzydełka: \(x_skrzydelka)\n",
  "Paluszki: \(x_paluszki)\n",
  "Zestaw próbny: \(x_zestaw_probny)\n"
];
