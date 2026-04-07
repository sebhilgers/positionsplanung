class Betonbauteil:
    """Einfaches Zustandsobjekt für die erste Testversion.

    Das Objekt speichert nur fachlich relevante Zustände.
    Die eigentlichen Regeln liegen bewusst außerhalb dieser Klasse.
    """

    def __init__(self, bauteiltyp: str):
        self.bauteiltyp = bauteiltyp
        self.flaeche = None
        self.lage = None
        self.feuchte = None
        self.frost = None
        self.tausalz = None
        self.meerwasser = None
        self.chemischer_angriff = None
        self.verschleiss = None

        self.expositionsklassen = []
        self.begruendungen = []
        self.mindestfestigkeitsklasse = None
        self.cmin_dur_mm = None

    def setze_parameter(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(f"Unbekanntes Attribut: {key}")
            setattr(self, key, value)

    def ist_grundsaetzlich_bewertbar(self) -> bool:
        benoetigt = [self.bauteiltyp, self.lage, self.feuchte]
        return all(wert is not None for wert in benoetigt)
