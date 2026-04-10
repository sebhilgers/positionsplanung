from positionsplanung.model import Betonbauteil

class Dauerhaftigkeitsbewerter:
    def bewerte_flaeche(self, flaeche):
        festigkeiten = [
            self.STRENGTH[k]
            for k in flaeche.expositionsklassen
            if k in self.STRENGTH
        ]

        deckungen = [
            self.CMIN_DUR[k]
            for k in flaeche.expositionsklassen
            if k in self.CMIN_DUR
        ]

        if festigkeiten:
            flaeche.mindestfestigkeitsklasse = max(
                festigkeiten,
                key=self.ORDER.index
            )

        if deckungen:
            flaeche.cmin_dur_mm = max(deckungen)

