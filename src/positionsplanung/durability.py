from positionsplanung.model import Betonbauteil


class Dauerhaftigkeitsbewerter:
    """Einfache Zuordnung fuer die erste Testversion.

    Achtung: Die Tabellen sind bewusst reduziert und dienen nur der Architekturprobe.
    """

    STRENGTH_BY_EXPOSURE = {
        "X0": "C12/15",
        "XC1": "C16/20",
        "XC2": "C16/20",
        "XC3": "C20/25",
        "XC4": "C25/30",
        "XD1": "C30/37",
        "XD2": "C35/45",
        "XD3": "C35/45",
        "XS1": "C30/37",
        "XS2": "C35/45",
        "XS3": "C35/45",
        "XF1": "C25/30",
        "XF3": "C30/37",
        "XF4": "C30/37",
        "XA1": "C25/30",
        "XA2": "C35/45",
        "XA3": "C35/45",
        "XM1": "C30/37",
        "XM2": "C30/37",
        "XM3": "C35/45",
    }

    CMIN_DUR_BY_EXPOSURE = {
        "XC1": 10,
        "XC2": 20,
        "XC3": 20,
        "XC4": 25,
        "XD1": 30,
        "XD2": 35,
        "XD3": 40,
        "XS1": 30,
        "XS2": 35,
        "XS3": 40,
        "XF1": 25,
        "XF3": 35,
        "XF4": 40,
        "XA1": 25,
        "XA2": 35,
        "XA3": 40,
    }

    ORDER = [
        "C12/15",
        "C16/20",
        "C20/25",
        "C25/30",
        "C30/37",
        "C35/45",
        "C40/50",
        "C45/55",
        "C50/60",
    ]

    def bewerte(self, bauteil: Betonbauteil) -> Betonbauteil:
        strength_values = []
        cover_values = []

        for exposure in bauteil.expositionsklassen:
            strength = self.STRENGTH_BY_EXPOSURE.get(exposure)
            if strength:
                strength_values.append(strength)

            cover = self.CMIN_DUR_BY_EXPOSURE.get(exposure)
            if cover is not None:
                cover_values.append(cover)

        if strength_values:
            bauteil.mindestfestigkeitsklasse = max(
                strength_values,
                key=self.ORDER.index,
            )

        if cover_values:
            bauteil.cmin_dur_mm = max(cover_values)

        return bauteil
