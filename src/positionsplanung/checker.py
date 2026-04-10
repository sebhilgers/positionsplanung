from .models import RechteckStuetzeEingabe, StuetzeAuswertung
from .rules import ALLE_REGELN


def pruefe_stuetze(eingabe: RechteckStuetzeEingabe) -> StuetzeAuswertung:
    if not isinstance(eingabe, RechteckStuetzeEingabe):
        raise TypeError("Die Eingabe muss eine RechteckStuetzeEingabe sein")

    regelergebnisse = [regel.pruefe(eingabe) for regel in ALLE_REGELN]
    return StuetzeAuswertung(eingabe, regelergebnisse)
