from positionsplanung.model import Betonbauteil


CHOICES = {
    "bauteiltyp": ["Decke", "Wand", "Stuetze", "Bodenplatte"],
    "flaeche": ["oben", "unten", "seite", "innen", "aussen"],
    "lage": ["innen", "aussen", "erdberuehrt", "wasserberuehrt"],
    "feuchte": [
        "trocken",
        "maessig_feucht",
        "wechselnd_nass_trocken",
        "dauerhaft_nass",
    ],
    "chemischer_angriff": ["nein", "XA1", "XA2", "XA3"],
    "verschleiss": ["nein", "XM1", "XM2", "XM3"],
}


QUESTIONS = {
    "flaeche": "Welche Flaeche soll betrachtet werden?",
    "lage": "Wo liegt die betrachtete Bauteilflaeche?",
    "feuchte": "Welche Feuchtebeanspruchung liegt vor?",
    "frost": "Liegt Frostbeanspruchung vor?",
    "tausalz": "Liegt Tausalzeinwirkung vor?",
    "meerwasser": "Liegt Meerwassereinwirkung vor?",
    "chemischer_angriff": "Liegt chemischer Angriff vor?",
    "verschleiss": "Liegt Verschleissbeanspruchung vor?",
}


class BauteilAbfrage:
    def offene_felder(self, bauteil: Betonbauteil) -> list[str]:
        felder = []

        if bauteil.flaeche is None:
            felder.append("flaeche")
        if bauteil.lage is None:
            felder.append("lage")
        if bauteil.feuchte is None:
            felder.append("feuchte")

        if bauteil.lage in {"aussen", "erdberuehrt", "wasserberuehrt"}:
            if bauteil.frost is None:
                felder.append("frost")
            if bauteil.meerwasser is None:
                felder.append("meerwasser")

        if bauteil.frost is True and bauteil.tausalz is None:
            felder.append("tausalz")
        elif bauteil.lage == "aussen" and bauteil.tausalz is None:
            felder.append("tausalz")

        if bauteil.chemischer_angriff is None:
            felder.append("chemischer_angriff")
        if bauteil.verschleiss is None:
            felder.append("verschleiss")

        return felder


    def interaktiv_befuellen(self, bauteil: Betonbauteil):
        for feld in self.offene_felder(bauteil):
            value = self._frage_feld(feld)
            setattr(bauteil, feld, value)
        return bauteil

    def _frage_feld(self, feld: str):
        if feld in CHOICES:
            return self._frage_auswahl(QUESTIONS[feld], CHOICES[feld])
        return self._frage_bool(QUESTIONS[feld])

    @staticmethod
    def _frage_bool(text: str) -> bool:
        while True:
            answer = input(f"{text} [j/n]: ").strip().lower()
            if answer in {"j", "ja", "y", "yes"}:
                return True
            if answer in {"n", "nein", "no"}:
                return False
            print("Bitte j oder n eingeben.")

    @staticmethod
    def _frage_auswahl(text: str, optionen: list[str]) -> str:
        while True:
            print(text)
            for index, option in enumerate(optionen, start=1):
                print(f"  {index}) {option}")
            answer = input("Auswahl: ").strip()

            if answer.isdigit():
                pos = int(answer) - 1
                if 0 <= pos < len(optionen):
                    value = optionen[pos]
                    return None if value == "nein" else value

            normalized = answer.lower()
            for option in optionen:
                if option.lower() == normalized:
                    return None if option == "nein" else option

            print("Ungueltige Eingabe. Bitte erneut versuchen.")
