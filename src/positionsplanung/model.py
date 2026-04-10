class Betonbauteil:
    """Einfaches Zustandsobjekt für die erste Testversion.

    Das Objekt speichert nur fachlich relevante Zustände.
    Die eigentlichen Regeln liegen bewusst außerhalb dieser Klasse.
    """

    def __init__(self, bauteiltyp):
        self.bauteiltyp = bauteiltyp
        self.flaechen = []

    def add_flaeche(self, flaeche):
        self.flaechen.append(flaeche)


    

class Bauteilflaeche:
    def __init__(self, name):
        self.name = name  # z.B. "oben", "unten", "aussen"

        # Eingaben
        self.lage = None
        self.feuchte = None
        self.frost = None
        self.tausalz = None
        self.meerwasser = None
        self.chemischer_angriff = None
        self.verschleiss = None

        # Ergebnisse
        self.expositionsklassen = []
        self.mindestfestigkeitsklasse = None
        self.cmin_dur_mm = None

