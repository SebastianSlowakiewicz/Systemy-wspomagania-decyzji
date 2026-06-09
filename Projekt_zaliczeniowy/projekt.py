import graphviz
from opyenxes.data_in.XUniversalParser import XUniversalParser
from collections import defaultdict


SCIEZKA_LOGU = 'Projekt_zaliczeniowy/repairexample.xes'
NAZWA_PLIKU_HEURYSTYKA = 'siec_heurystyczna'
NAZWA_PLIKU_BPMN = 'graf_alpha_bpmn'

PROG_CZESTOSCI_AKTYWNOSCI = 0  
PROG_CZESTOSCI_PRZEJSC = 0 

TYPY_ANALIZY = {
    'heurystyka': 'heuristic',
    'alpha': 'alpha'
}

WYBRANA_METODA = TYPY_ANALIZY['alpha'] 


try:
    with open(SCIEZKA_LOGU) as plik_z_logiem:
        dane_logu = XUniversalParser().parse(plik_z_logiem)[0]
except FileNotFoundError:
    print(f"Błąd: Plik '{SCIEZKA_LOGU}' nie został znaleziony.")
    exit()
except Exception as e:
    print(f"Błąd podczas parsowania pliku XES: {e}")
    exit()

print(f"Log '{SCIEZKA_LOGU}' wczytany pomyślnie.")


dziennik_przeplywu = []
for slad in dane_logu:
    slad_procesu = []
    for zdarzenie in slad:
        try:
            atrybuty = zdarzenie.get_attributes()
            if 'Activity' in atrybuty:
                 nazwa_aktywnosci = atrybuty['Activity'].get_value()
                 slad_procesu.append(nazwa_aktywnosci)
            elif 'concept:name' in atrybuty:
                 nazwa_aktywnosci = atrybuty['concept:name'].get_value()
                 slad_procesu.append(nazwa_aktywnosci)
        except Exception as e:
            print(f"Ostrzeżenie: Problem w śladzie {dane_logu.index(slad)}: {e}")

    if slad_procesu: 
        dziennik_przeplywu.append(slad_procesu)

if not dziennik_przeplywu:
    print("Błąd: Nie udało się wyekstrahować śladów.")
    exit()

print(f"Wyekstrahowano {len(dziennik_przeplywu)} śladów.")


licznik_aktywnosci = defaultdict(int)
licznik_przejsc = defaultdict(int)
relacje_sukcesji = defaultdict(set) 

for slad in dziennik_przeplywu:
    if not slad: continue 

    for akt in slad:
        licznik_aktywnosci[akt] += 1

    for i in range(len(slad) - 1):
        akt_zrodlowa = slad[i]
        akt_docelowa = slad[i+1]
        przejscie = (akt_zrodlowa, akt_docelowa)
        licznik_przejsc[przejscie] += 1
        relacje_sukcesji[akt_zrodlowa].add(akt_docelowa)

wszystkie_aktywnosci = set(licznik_aktywnosci.keys())
if not wszystkie_aktywnosci:
    print("Błąd: Nie znaleziono żadnych aktywności.")
    exit()

print(f"Znaleziono {len(wszystkie_aktywnosci)} unikalnych aktywności.")


def generuj_graf_heurystyczny(mapa_aktywnosci, mapa_przejsc, sukcesja_bezposrednia, prog_akt, prog_przejsc, baza_pliku):
    przefiltrowane_akt = {akt for akt, ile in mapa_aktywnosci.items() if ile >= prog_akt}
    if not przefiltrowane_akt:
        print(f"Ostrzeżenie: Brak aktywności spełniających próg {prog_akt}.")
        return None

    przefiltrowane_przejscia = {prz: ile for prz, ile in mapa_przejsc.items()
                                if ile >= prog_przejsc and
                                prz[0] in przefiltrowane_akt and
                                prz[1] in przefiltrowane_akt}

    G = graphviz.Digraph(comment='Heuristic Net')
    G.graph_attr['rankdir'] = 'LR' 
    G.node_attr['shape'] = 'box'   
    G.node_attr['style'] = 'rounded,filled'
    G.node_attr['fillcolor'] = "#9CFF8D" 

    min_akt = min(mapa_aktywnosci.values()) if mapa_aktywnosci else 1
    max_akt = max(mapa_aktywnosci.values()) if mapa_aktywnosci else 1
    min_prz = min(przefiltrowane_przejscia.values()) if przefiltrowane_przejscia else 1
    max_prz = max(przefiltrowane_przejscia.values()) if przefiltrowane_przejscia else 1

    for akt in przefiltrowane_akt:
        ile = mapa_aktywnosci[akt]
        etykieta = f"{akt}\n({ile})"

        odcien = 0
        if max_akt > min_akt:
             norm_czestosc = (ile - min_akt) / (max_akt - min_akt)
             odcien = 99 - int(norm_czestosc * 99) 
        else: 
             odcien = 50 

        hex_odcien = hex(odcien)[2:].zfill(2)
        kolor_wezla = f"#FF9933{hex_odcien}" 

        G.node(akt, label=etykieta, fillcolor=kolor_wezla)

    for (zrodlo, cel), ile in przefiltrowane_przejscia.items():
        grubosc = 1.0
        if max_prz > min_prz:
             norm_grubosc = (ile - min_prz) / (max_prz - min_prz)
             grubosc = 1 + norm_grubosc * 5
        elif ile > 0: 
            grubosc = 2.0 

        G.edge(zrodlo, cel, label=str(ile), penwidth=str(grubosc))

    w_startowe = {prz[0] for prz in przefiltrowane_przejscia}
    w_koncowe = {prz[1] for prz in przefiltrowane_przejscia}

    aktywnosci_start = przefiltrowane_akt - w_koncowe
    aktywnosci_koniec = przefiltrowane_akt - w_startowe

    if aktywnosci_start:
        G.node("start", shape="circle", label="", fillcolor="#41F241", width="0.3", fixedsize="true") 
        for akt in aktywnosci_start:
            G.edge("start", akt)

    if aktywnosci_koniec:
        G.node("end", shape="doublecircle", label="", fillcolor="#F93B57", width="0.3", fixedsize="true") 
        for akt in aktywnosci_koniec:
            try:
                 G.node(akt) 
                 G.edge(akt, "end")
            except KeyError: 
                 pass

    try:
        pl_dot = f"{baza_pliku}_filtrowany_akt{prog_akt}_trans{prog_przejsc}.gv"
        pl_png = f"{baza_pliku}_filtrowany_akt{prog_akt}_trans{prog_przejsc}.png"
        G.render(pl_dot, view=False, format='png', outfile=pl_png)
        print(f"Graf heurystyczny zapisany jako '{pl_png}'")
        return G 
    except Exception as e:
        print(f"Błąd renderowania Graphviz: {e}")
        return None


def oblicz_relacje_alpha(dziennik, zbior_aktywnosci):
    sukcesja = defaultdict(set) 
    macierz_sladu = defaultdict(lambda: defaultdict(str)) 

    for slad in dziennik:
        for i in range(len(slad) - 1):
            sukcesja[slad[i]].add(slad[i+1])

    przyczynowosc = defaultdict(set) 
    rownoleglosc = set()           

    lista_akt = sorted(list(zbior_aktywnosci)) 
    for akt_a in lista_akt:
        for akt_b in lista_akt:
            a_po_b = akt_b in sukcesja.get(akt_a, set())
            b_po_a = akt_a in sukcesja.get(akt_b, set())

            if a_po_b and not b_po_a:
                macierz_sladu[akt_a][akt_b] = "->"
                przyczynowosc[akt_a].add(akt_b)
            elif not a_po_b and b_po_a:
                macierz_sladu[akt_a][akt_b] = "<-"
            elif a_po_b and b_po_a:
                macierz_sladu[akt_a][akt_b] = "||"
                if (akt_a, akt_b) not in rownoleglosc and (akt_b, akt_a) not in rownoleglosc:
                     rownoleglosc.add((akt_a, akt_b))
                     rownoleglosc.add((akt_b, akt_a)) 
            else: 
                macierz_sladu[akt_a][akt_b] = "#"

    start_formalny = zbior_aktywnosci.copy()
    koniec_formalny = zbior_aktywnosci.copy()
    for akt_a in zbior_aktywnosci:
        for akt_b in zbior_aktywnosci:
             if akt_a == akt_b: continue
             if macierz_sladu[akt_b][akt_a] in ["->", "||"]:
                 start_formalny.discard(akt_a)
             if macierz_sladu[akt_a][akt_b] in ["->", "||"]:
                 koniec_formalny.discard(akt_a)

    odwrotna_przyczynowosc = defaultdict(set)
    for zrodlo, cele in przyczynowosc.items():
        for cel in cele:
            odwrotna_przyczynowosc[cel].add(zrodlo)

    print("Relacje Alpha obliczone.")
    return przyczynowosc, rownoleglosc, start_formalny, koniec_formalny, odwrotna_przyczynowosc

class MojGraf(graphviz.Digraph):
    def __init__(self, *args, **kwargs):
        super(MojGraf, self).__init__(*args, **kwargs)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'box' 
        self.node_attr['style'] = 'rounded'
        self.graph_attr['nodesep'] = '0.6' 
        self.edge_attr.update(penwidth='1.5') 
        self._licznik_bramek = 0 

    def _unikalna_nazwa_bramki(self, prefiks, podpowiedz=""):
        self._licznik_bramek += 1
        return f"{prefiks}_{self._licznik_bramek}_{podpowiedz}"

    def dodaj_aktywnosc(self, nazwa, **kwargs):
         domyslne = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': "#FFFF55"}
         domyslne.update(kwargs)
         super(MojGraf, self).node(nazwa, **domyslne)

    def dodaj_zdarzenie(self, nazwa, **kwargs):
        domyslne = {'shape': 'circle', 'label': '', 'width': '0.3', 'fixedsize': 'true'}
        if 'start' in nazwa.lower():
             domyslne.update({'fillcolor': "#51E851", 'style': 'filled'})
        elif 'end' in nazwa.lower():
             domyslne.update({'shape': 'doublecircle', 'fillcolor': "#F44862", 'style': 'filled'})
        domyslne.update(kwargs)
        super(MojGraf, self).node(nazwa, **domyslne)

    def dodaj_bramke(self, nazwa, etykieta, **kwargs):
         domyslne = {
             'shape': 'diamond', 'width': '.5', 'height': '.5', 
             'fixedsize': 'true', 'fontsize': '20', 'label': etykieta,
             'style': 'filled', 'fillcolor': '#E0E0E0' 
             }
         domyslne.update(kwargs)
         super(MojGraf, self).node(nazwa, **domyslne)

    def dodaj_bramke_rozdzielajaca(self, zrodlo, cele, typ_bramki, rel_rownolegle):
        podpowiedz = f"{zrodlo}->{'_'.join(sorted(list(cele)))}" 
        jest_rownolegly_split = False

        if len(cele) > 1:
             lista_celow = sorted(list(cele))
             jest_rownolegly_split = any((t1, t2) in rel_rownolegle for i, t1 in enumerate(lista_celow) for t2 in lista_celow[i+1:])

        nazwa_bramki = self._unikalna_nazwa_bramki(f"{typ_bramki}s", podpowiedz)

        if typ_bramki == "AND" or (typ_bramki == "AUTO" and jest_rownolegly_split):
            self.dodaj_bramke(nazwa_bramki, '+')
        else: 
            self.dodaj_bramke(nazwa_bramki, '×')

        super(MojGraf, self).edge(zrodlo, nazwa_bramki)
        for cel in cele:
            super(MojGraf, self).edge(nazwa_bramki, cel)
        return nazwa_bramki 

    def dodaj_bramke_laczaca(self, zrodla, cel, typ_bramki, rel_rownolegle):
        podpowiedz = f"{'_'.join(sorted(list(zrodla)))}->{cel}"
        jest_rownolegly_merge = False
        if len(zrodla) > 1:
            lista_zrodel = sorted(list(zrodla))
            jest_rownolegly_merge = any((s1, s2) in rel_rownolegle for i, s1 in enumerate(lista_zrodel) for s2 in lista_zrodel[i+1:])

        nazwa_bramki = self._unikalna_nazwa_bramki(f"{typ_bramki}m", podpowiedz)

        if typ_bramki == "AND" or (typ_bramki == "AUTO" and jest_rownolegly_merge):
            self.dodaj_bramke(nazwa_bramki, '+')
        else: 
            self.dodaj_bramke(nazwa_bramki, '×')

        super(MojGraf, self).edge(nazwa_bramki, cel)
        for zrodlo in zrodla:
            super(MojGraf, self).edge(zrodlo, nazwa_bramki)
        return nazwa_bramki

def generuj_graf_bpmn(przyczynowosc, rownoleglosc, start_events, end_events, inv_causality, zbior_aktywnosci, baza_pliku):
    G = MojGraf(comment='Alpha Miner BPMN')
    krawedzie_do_dodania = set() 

    for akt in zbior_aktywnosci:
        G.dodaj_aktywnosc(akt)

    for zrodlo, cele in przyczynowosc.items():
        if len(cele) > 1:
            G.dodaj_bramke_rozdzielajaca(zrodlo, cele, "AUTO", rownoleglosc)
        elif len(cele) == 1:
            cel = list(cele)[0]
            krawedzie_do_dodania.add((zrodlo, cel))

    for cel, zrodla in inv_causality.items():
        if len(zrodla) > 1:
            G.dodaj_bramke_laczaca(zrodla, cel, "AUTO", rownoleglosc)
            for zrodlo in zrodla:
                 krawedzie_do_dodania.discard((zrodlo, cel))
        
    for zrodlo, cel in krawedzie_do_dodania:
             G.edge(zrodlo, cel)

    G.dodaj_zdarzenie("start")
    if len(start_events) > 1:
        G.dodaj_bramke_rozdzielajaca("start", start_events, "AUTO", rownoleglosc)
    elif len(start_events) == 1:
        G.edge("start", list(start_events)[0])
    
    G.dodaj_zdarzenie("end")
    if len(end_events) > 1:
        G.dodaj_bramke_laczaca(end_events, "end", "AUTO", rownoleglosc)
    elif len(end_events) == 1:
        G.edge(list(end_events)[0], "end")
    
    try:
        pl_dot = f"{baza_pliku}.gv"
        pl_png = f"{baza_pliku}.png"
        G.render(pl_dot, view=False, format='png', outfile=pl_png)
        print(f"Graf BPMN (Alpha) zapisany jako '{pl_png}'")
        return G
    except Exception as e:
        print(f"Błąd renderowania BPMN: {e}")
        return None


if __name__ == "__main__":
    if WYBRANA_METODA == 'heuristic':
        print("\n--- Generowanie Grafu Heurystycznego ---")
        generuj_graf_heurystyczny(
            licznik_aktywnosci,
            licznik_przejsc,
            relacje_sukcesji,
            PROG_CZESTOSCI_AKTYWNOSCI,
            PROG_CZESTOSCI_PRZEJSC,
            NAZWA_PLIKU_HEURYSTYKA
        )
    elif WYBRANA_METODA == 'alpha':
        print("\n--- Generowanie Grafu Algorytmu Alpha ---")
        przyczynowosc, rownoleglosc, start_events, end_events, inv_causality = oblicz_relacje_alpha(
            dziennik_przeplywu,
            wszystkie_aktywnosci
        )
        generuj_graf_bpmn(
            przyczynowosc,
            rownoleglosc,
            start_events,
            end_events,
            inv_causality,
            wszystkie_aktywnosci,
            NAZWA_PLIKU_BPMN
        )
    print("\n--- Zakończono ---")