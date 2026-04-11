# bauteilposition.py

class BauteilPosition:
    def __init__(
        self,
        positionsnummer: str,
        bezeichnung: str,
        beschreibung: str | None = None,
    ) -> None:
        self.positionsnummer = positionsnummer
        self.bezeichnung = bezeichnung
        self.beschreibung = beschreibung