from positionsplanung.model import Betonbauteil, Bauteilflaeche
from positionsplanung.questionnaire import BauteilAbfrage, CHOICES
from positionsplanung.rules import Expositionsbewerter
from positionsplanung.durability import Dauerhaftigkeitsbewerter
from positionsplanung.report import build_report


def _frage_bauteiltyp() -> str:
    optionen = CHOICES["bauteiltyp"]
    while True:
        print("Welcher Bauteiltyp soll bewertet werden?")
        for index, option in enumerate(optionen, start=1):
            print(f"  {index}) {option}")
        answer = input("Auswahl: ").strip()

        if answer.isdigit():
            pos = int(answer) - 1
            if 0 <= pos < len(optionen):
                return optionen[pos]

        for option in optionen:
            if option.lower() == answer.lower():
                return option

        print("Ungueltige Eingabe. Bitte erneut versuchen.")

def erfasse_flaeche():
    name = input("Flächenname (z.B. oben/unten/aussen): ")
    f = Bauteilflaeche(name)

    f.lage = input("Lage [innen/aussen]: ")
    f.feuchte = input("Feuchte: ")
    f.frost = frage_bool("Frost?")
    f.tausalz = frage_bool("Tausalz?")
    f.meerwasser = frage_bool("Meerwasser?")

    return f


def erfasse_bauteil():
    typ = input("Bauteiltyp: ")
    bauteil = Betonbauteil(typ)

    while True:
        flaeche = erfasse_flaeche()
        bauteil.add_flaeche(flaeche)

        if not frage_bool("Weitere Fläche hinzufügen?"):
            break

    return bauteil


def main():
    print("positionsplanung - Testversion")
    print()

    bauteil = erfasse_bauteil()

    exp = Expositionsbewerter()
    dur = Dauerhaftigkeitsbewerter()

    for flaeche in bauteil.flaechen:
        exp.bewerte_flaeche(flaeche)
        dur.bewerte_flaeche(flaeche)

    print()
    print(build_report(bauteil))


if __name__ == "__main__":
    main()
