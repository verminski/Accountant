from ast import literal_eval

def data_read():
    try:
        with open ("magazyn.txt", "r") as file:
            magazyn = literal_eval(file.read())
    except FileNotFoundError:
        print("Brak pliku 'magazyn.txt'. Stworzenie pliku 'magazyn.txt")
        magazyn = {
            "pieczywo": {"cena": 2.50, "ilosc": 10},
            "nabiał": {"cena": 3.50, "ilosc": 5},
            "owoc": {"cena": 4.50, "ilosc": 3},
            "warzywo": {"cena": 5.50, "ilosc": 1},
        }
    try:
        with open("saldo.txt", "r") as file:
            saldo = float(file.read())
    except FileNotFoundError:
        print("Brak pliku 'saldo.txt'. Stworzenie pliku 'saldo.txt'")
        saldo = 1000.00
    try:
        with open("historia.txt", "r") as file:
            historia = file.read().splitlines()
    except FileNotFoundError:
        print("Brak pliku 'historia.txt'. Stworzenie pliku 'historia.txt'")
        historia = []

    return magazyn, saldo, historia

def data_write(magazyn, saldo, historia):
    with open("magazyn.txt", "w") as file:
        file.write(str(magazyn))
    with open("saldo.txt", "w") as file:
        file.write(str(saldo))
    with open("historia.txt", "w") as file:
        file.write("\n".join(historia))
