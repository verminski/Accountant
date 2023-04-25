from funkcje_do_magazyn import data_read, data_write

class Manager:
    def __init__(self):
        self.magazyn, self.saldo, self.historia = data_read()
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
            return cb
        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Akcja niezdefiniowana.")
        else:
            self.actions[name](self)

manager = Manager()

@manager.assign("saldo")
def saldo(manager):
    print(f"\nObecny stan salda wynosi: {manager.saldo} PLN")
    print("\nDostępne opcje:")
    print("\ndodaj - dodaj kwotę do konta")
    print("odejmij - odejmij kwotę z konta\n")
    opcja_saldo = input("Podaj opcję 'dodaj' lub 'odejmij': ")
    if opcja_saldo == "dodaj":
        kwota = float(input("Podaj kwotę do dodania: "))
        manager.saldo += kwota
        manager.historia.append(f"[saldo -> {opcja_saldo}] Dodano {kwota} PLN")
        print(f"Saldo zostało zaktualizowane: {manager.saldo} PLN. Powrót do menu głównego.")
    elif opcja_saldo == "odejmij":
        kwota = float(input("Podaj kwotę do odjęcia: "))
        manager.saldo -= kwota
        manager.historia.append(f"[saldo -> {opcja_saldo})] Odjęto {kwota} PLN")
        print(f"Saldo zostało zaktualizowane: {manager.saldo} PLN. Powrót do menu głównego")
    else:
        print("Błędna komenda. Wpisz 'dodaj' lub 'odejmij'.")

@manager.assign("sprzedaz")
def sprzedaz(manager):
    produkt = input("Podaj nazwę produktu: ")
    cena = float(input("Podaj cenę produktu: "))
    ilosc = int(input("Podaj ilosc produktu: "))
    if produkt in manager.magazyn:
        if manager.magazyn[produkt]["ilosc"] >= ilosc:
            manager.magazyn[produkt]["ilosc"] -= ilosc
            manager.saldo += cena * ilosc
            manager.historia.append(f"sprzedaz -> Sprzedano {ilosc} sztuk {produkt} za {cena} PLN")
            print(f"Saldo po operacji: {manager.saldo} PLN")
        else:
            print("Nie ma odpowiedniej ilości na magazynie!")
    else:
        print(f"\nNie ma produktu '{produkt}' w magazynie! Powrót do Menu Głównego.")

@manager.assign("zakup")
def zakup(manager):
    produkt_buy = input("Podaj nazwę produktu: ")
    if produkt_buy in manager.magazyn:
        print("Nie można dodać tego samego produktu!")
    else:
        cena_buy = float(input("Podaj cenę produktu: "))
        ilosc_buy = int(input("Podaj ilosc produktu: "))
        if cena_buy * ilosc_buy >= manager.saldo:
            print("Brak środków na koncie, operacja anulowana.")
        else:
            manager.magazyn[produkt_buy] = {"cena": cena_buy, "ilosc": ilosc_buy}
            manager.saldo -= cena_buy * ilosc_buy
            manager.historia.append(f"[zakup] Kupiono {ilosc_buy} sztuk {produkt_buy} za {cena_buy} PLN")
            print(f"Produkt dodany do magazynu. Saldo po operacji: {manager.saldo}")

@manager.assign("konto")
def konto(manager):
    print(f"Stan konta: {manager.saldo:.2f} PLN")

@manager.assign("lista")
def lista(manager):
    print("Stan magazynu:\n")
    for produkt, dane in manager.magazyn.items():
        print(f"{produkt} - cena: {dane['cena']}, ilosc : {dane['ilosc']}")

@manager.assign("magazyn")
def magazyn(manager):
    produkt = input("Podaj nazwę produktu: ")
    if produkt in manager.magazyn:
        print(f"{produkt} - cena: {manager.magazyn[produkt]['cena']} PLN, ilosc: {manager.magazyn[produkt]['ilosc']}")
    else:
        print(f"Nie ma produktu '{produkt}' w magazynie!")

@manager.assign("przeglad")
def przeglad(manager):
    print("Podaj zakres przeglądu\n")
    od = input("Podaj początek zakresu (od zera): ")
    do = input("Podaj koniec zakresu: ")
    if od == "" and do == "":
        for akcja in manager.historia:
            print(akcja)
    elif od == "" or do == "":
        print("Błąd. Podaj poprawnie dane.")
    elif int(od) < 0 or int(do) < 0:
        print("Zakres nie może być mniejszy od zera!")
    elif int(do) > len(manager.historia):
        print(f"Zakres przeglądu jest poza zakresem historii akcji."
              f" Liczba wpisów w historii wynosi: {len(manager.historia)}")
    elif int(od) >= int(do):
        print(f"Zakres przeglądu jest poza zakresem historii akcji. "
              f"Liczba wpisów w historii wynosi: {len(manager.historia)}")
    else:
        for akcja in manager.historia[int(od):int(do)]:
            print(akcja)

@manager.assign("koniec")
def koniec(manager):
        data_write(manager.magazyn, manager.saldo, manager.historia)
        print("Dane zostały zapisane")
        print("Koniec programu.")

while True:
        print("\nWitam w systemie księgowym!\n\nDostępne opcje:")
        print("\n'saldo' - Zaktualizuj stan salda.")
        print("'sprzedaz' - Sprzedaż produktów w magazynie.")
        print("'zakup' - Kup nowe produkty do magazynu.")
        print("'konto' - Wyświetl stan konta.")
        print("'lista' - Wyświetl stan magazynu.")
        print("'magazyn' - Wyświetl stan magazynu. dla konkretnego produktu.")
        print("'przeglad' - Wyświetl historię magazynu.")
        print("'koniec' - Zakończ działanie programu.")

        opcja = input("\nWybierz opcję: ")
        if opcja == "koniec":
            manager.execute(opcja)
            break
        else:
            manager.execute(opcja)