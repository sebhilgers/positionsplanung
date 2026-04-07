from positionsplanung.model import Betonbauteil


class Expositionsbewerter:
    """Regelbasierte, bewusst einfache Testlogik."""

    def bewerte(self, bauteil: Betonbauteil) -> list[str]:
        klassen = []
        gruende = []

        self._bewerte_x0_und_xc(bauteil, klassen, gruende)
        self._bewerte_xd(bauteil, klassen, gruende)
        self._bewerte_xs(bauteil, klassen, gruende)
        self._bewerte_xf(bauteil, klassen, gruende)
        self._bewerte_xa(bauteil, klassen, gruende)
        self._bewerte_xm(bauteil, klassen, gruende)

        bauteil.expositionsklassen = sorted(set(klassen))
        bauteil.begruendungen = gruende
        return bauteil.expositionsklassen

    def _bewerte_x0_und_xc(self, bauteil, klassen, gruende):
        if bauteil.lage == "innen" and bauteil.feuchte == "trocken":
            klassen.append("XC1")
            gruende.append("Innenbauteil mit trockener Umgebung -> XC1")
            return

        if bauteil.feuchte == "maessig_feucht":
            klassen.append("XC2")
            gruende.append("Maessig feuchte Umgebung -> XC2")
            return

        if bauteil.feuchte == "dauerhaft_nass":
            klassen.append("XC3")
            gruende.append("Dauerhaft feuchte Umgebung -> XC3")
            return

        if bauteil.feuchte == "wechselnd_nass_trocken":
            klassen.append("XC4")
            gruende.append("Wechselnd nass/trocken -> XC4")
            return

    def _bewerte_xd(self, bauteil, klassen, gruende):
        if bauteil.tausalz is not True:
            return

        if bauteil.feuchte == "maessig_feucht":
            klassen.append("XD1")
            gruende.append("Tausalzeinwirkung bei maessig feuchter Umgebung -> XD1")
            return

        if bauteil.feuchte == "dauerhaft_nass":
            klassen.append("XD2")
            gruende.append("Tausalzeinwirkung bei dauerhaft feuchter Umgebung -> XD2")
            return

        klassen.append("XD3")
        gruende.append("Tausalzeinwirkung mit wechselnder Befeuchtung -> XD3")

    def _bewerte_xs(self, bauteil, klassen, gruende):
        if bauteil.meerwasser is not True:
            return

        if bauteil.feuchte == "maessig_feucht":
            klassen.append("XS1")
            gruende.append("Meerwassereinwirkung bei luftseitiger Salzbelastung -> XS1")
            return

        if bauteil.feuchte == "dauerhaft_nass":
            klassen.append("XS2")
            gruende.append("Dauernder Meerwasserkontakt -> XS2")
            return

        klassen.append("XS3")
        gruende.append("Spritz-/Wechselzone bei Meerwassereinwirkung -> XS3")

    def _bewerte_xf(self, bauteil, klassen, gruende):
        if bauteil.frost is not True:
            return

        if bauteil.tausalz is True:
            klassen.append("XF4")
            gruende.append("Frostangriff mit Tausalzen -> XF4")
            return

        if bauteil.feuchte in {"trocken", "maessig_feucht"}:
            klassen.append("XF1")
            gruende.append("Frostangriff ohne Tausalz bei maessiger Wassersaettigung -> XF1")
            return

        klassen.append("XF3")
        gruende.append("Frostangriff ohne Tausalz bei hoher Wassersaettigung -> XF3")

    def _bewerte_xa(self, bauteil, klassen, gruende):
        if bauteil.chemischer_angriff:
            klassen.append(bauteil.chemischer_angriff)
            gruende.append(f"Chemischer Angriff angegeben -> {bauteil.chemischer_angriff}")

    def _bewerte_xm(self, bauteil, klassen, gruende):
        if bauteil.verschleiss:
            klassen.append(bauteil.verschleiss)
            gruende.append(f"Verschleissbeanspruchung angegeben -> {bauteil.verschleiss}")
