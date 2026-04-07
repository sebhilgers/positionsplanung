from positionsplanung.model import Betonbauteil
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


def main():
    print("positionsplanung - Testversion")
    print()

    bauteiltyp = _frage_bauteiltyp()
    bauteil = Betonbauteil(bauteiltyp)

    abfrage = BauteilAbfrage()
    abfrage.interaktiv_befuellen(bauteil)

    expositionsbewerter = Expositionsbewerter()
    dauerhaftigkeitsbewerter = Dauerhaftigkeitsbewerter()

    expositionsbewerter.bewerte(bauteil)
    dauerhaftigkeitsbewerter.bewerte(bauteil)

    print()
    print(build_report(bauteil))


if __name__ == "__main__":
    main()
