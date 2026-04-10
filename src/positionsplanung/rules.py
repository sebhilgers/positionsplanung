from typing import Callable

from .config import (
    FUEHRBARKEIT_KLEINSTE_ABMESSUNG_MM,
    KLEINE_QUERSCHNITT_LAENGE_MM,
    KLEINE_QUERSCHNITT_MINDSTABMESSUNG_MM,
    MINDESTABMESSUNG_MM,
    SCHLANKHEITSINDIKATOR_WARNUNG,
    SEITENVERHAELTNIS_WARNUNG,
)
from .models import RegelErgebnis, RegelStatus, RechteckStuetzeEingabe


class Regel:
    def __init__(
        self,
        regel_id: str,
        titel: str,
        funktion: Callable[[RechteckStuetzeEingabe], RegelErgebnis],
    ) -> None:
        self.regel_id = regel_id
        self.titel = titel
        self._funktion = funktion

    def pruefe(self, eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
        return self._funktion(eingabe)


def _r001_grundwerte_positiv(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    fehler = []
    if eingabe.breite_mm <= 0:
        fehler.append("Breite muss größer als 0 sein")
    if eingabe.hoehe_mm <= 0:
        fehler.append("Höhe muss größer als 0 sein")
    if eingabe.laenge_mm <= 0:
        fehler.append("Länge muss größer als 0 sein")

    if fehler:
        return RegelErgebnis(
            regel_id="R001",
            titel="Grundwerte positiv",
            status=RegelStatus.NICHT_ERFUELLT,
            meldung="; ".join(fehler),
            empfehlung="Prüfen Sie die Eingabewerte und stellen Sie sicher, dass alle Dimensionen größer als 0 mm sind.",
        )

    return RegelErgebnis(
        regel_id="R001",
        titel="Grundwerte positiv",
        status=RegelStatus.OK,
        meldung="Alle Grundmaße sind positiv.",
        empfehlung="",
    )


def _r002_mindestabmessung_eingehalten(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if eingabe.kleinste_abmessung_mm < MINDESTABMESSUNG_MM:
        return RegelErgebnis(
            regel_id="R002",
            titel="Mindestabmessung eingehalten",
            status=RegelStatus.NICHT_ERFUELLT,
            meldung=(
                f"Die kleinste Abmessung {eingabe.kleinste_abmessung_mm:.1f} mm liegt unter dem"
                f" Mindestwert von {MINDESTABMESSUNG_MM:.0f} mm."
            ),
            empfehlung=(
                f"Erhöhen Sie die Breite oder Höhe auf mindestens {MINDESTABMESSUNG_MM:.0f} mm."
            ),
        )

    return RegelErgebnis(
        regel_id="R002",
        titel="Mindestabmessung eingehalten",
        status=RegelStatus.OK,
        meldung="Die Mindestabmessung ist erfüllt.",
        empfehlung="",
    )


def _r003_seitenverhaeltnis_unauffaellig(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if eingabe.seitenverhaeltnis > SEITENVERHAELTNIS_WARNUNG:
        return RegelErgebnis(
            regel_id="R003",
            titel="Seitenverhältnis unauffällig",
            status=RegelStatus.WARNUNG,
            meldung=(
                f"Das Seitenverhältnis von {eingabe.seitenverhaeltnis:.2f} liegt über"
                f" der Schwelle von {SEITENVERHAELTNIS_WARNUNG:.1f}."
            ),
            empfehlung=(
                "Achten Sie auf die Bewehrungsführung und prüfen Sie, ob ein annähernd"
                " quadratischer Querschnitt möglich ist."
            ),
        )

    return RegelErgebnis(
        regel_id="R003",
        titel="Seitenverhältnis unauffällig",
        status=RegelStatus.OK,
        meldung="Das Seitenverhältnis ist unauffällig.",
        empfehlung="",
    )


def _r004_schlankheitsindikator_unauffaellig(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if eingabe.schlankheitsindikator > SCHLANKHEITSINDIKATOR_WARNUNG:
        return RegelErgebnis(
            regel_id="R004",
            titel="Schlankheitsindikator unauffällig",
            status=RegelStatus.WARNUNG,
            meldung=(
                f"Der Schlankheitsindikator von {eingabe.schlankheitsindikator:.2f}"
                f" übersteigt die Schwelle von {SCHLANKHEITSINDIKATOR_WARNUNG:.1f}."
            ),
            empfehlung=(
                "Beachten Sie, dass dies ein Vorprüfwert ist; eine genauere statische"
                " Überprüfung sollte erfolgen."
            ),
        )

    return RegelErgebnis(
        regel_id="R004",
        titel="Schlankheitsindikator unauffällig",
        status=RegelStatus.OK,
        meldung="Der Schlankheitsindikator ist im erwarteten Bereich.",
        empfehlung="",
    )


def _r005_kleiner_querschnitt_bei_grosser_laenge(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if (
        eingabe.kleinste_abmessung_mm < KLEINE_QUERSCHNITT_MINDSTABMESSUNG_MM
        and eingabe.laenge_mm > KLEINE_QUERSCHNITT_LAENGE_MM
    ):
        return RegelErgebnis(
            regel_id="R005",
            titel="Kleiner Querschnitt bei großer Länge",
            status=RegelStatus.WARNUNG,
            meldung=(
                f"Die Stütze hat eine kleine Abmessung von {eingabe.kleinste_abmessung_mm:.1f} mm "
                f"und eine Länge von {eingabe.laenge_mm:.0f} mm."
            ),
            empfehlung=(
                "Prüfen Sie die konstruktive Führung der Bewehrung und die Knotenausbildung."
            ),
        )

    return RegelErgebnis(
        regel_id="R005",
        titel="Kleiner Querschnitt bei großer Länge",
        status=RegelStatus.OK,
        meldung="Die Kombination aus Querschnitt und Länge ist unauffällig.",
        empfehlung="",
    )


def _r006_betonklasse_vorhanden(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if not eingabe.betonklasse:
        return RegelErgebnis(
            regel_id="R006",
            titel="Betonklasse vorhanden",
            status=RegelStatus.NICHT_BEWERTET,
            meldung="Die Betonklasse fehlt, daher kann diese Regel nicht bewertet werden.",
            empfehlung="Geben Sie eine Betonklasse an, um die Bewertung zu vervollständigen.",
        )

    return RegelErgebnis(
        regel_id="R006",
        titel="Betonklasse vorhanden",
        status=RegelStatus.OK,
        meldung="Die Betonklasse ist angegeben.",
        empfehlung="",
    )


def _r007_expositionsklasse_vorhanden(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if not eingabe.expositionsklasse:
        return RegelErgebnis(
            regel_id="R007",
            titel="Expositionsklasse vorhanden",
            status=RegelStatus.NICHT_BEWERTET,
            meldung=(
                "Die Expositionsklasse fehlt, daher kann diese Regel nicht bewertet werden."
            ),
            empfehlung="Geben Sie eine Expositionsklasse an, um die Bewertung zu vervollständigen.",
        )

    return RegelErgebnis(
        regel_id="R007",
        titel="Expositionsklasse vorhanden",
        status=RegelStatus.OK,
        meldung="Die Expositionsklasse ist angegeben.",
        empfehlung="",
    )


def _r008_konstruktive_fuehrbarkeit(eingabe: RechteckStuetzeEingabe) -> RegelErgebnis:
    if eingabe.kleinste_abmessung_mm < FUEHRBARKEIT_KLEINSTE_ABMESSUNG_MM:
        return RegelErgebnis(
            regel_id="R008",
            titel="Konstruktive Führbarkeit grob plausibel",
            status=RegelStatus.WARNUNG,
            meldung=(
                f"Die kleinste Abmessung von {eingabe.kleinste_abmessung_mm:.1f} mm "
                f"kann die Bewehrungsführung kritisch machen."
            ),
            empfehlung=(
                "Prüfen Sie die Bewehrungsführung und Knotenausbildung in der Ausführung."
            ),
        )

    return RegelErgebnis(
        regel_id="R008",
        titel="Konstruktive Führbarkeit grob plausibel",
        status=RegelStatus.OK,
        meldung="Die konstruktive Führbarkeit wirkt unauffällig.",
        empfehlung="",
    )


ALLE_REGELN = [
    Regel("R001", "Grundwerte positiv", _r001_grundwerte_positiv),
    Regel("R002", "Mindestabmessung eingehalten", _r002_mindestabmessung_eingehalten),
    Regel("R003", "Seitenverhältnis unauffällig", _r003_seitenverhaeltnis_unauffaellig),
    Regel("R004", "Schlankheitsindikator unauffällig", _r004_schlankheitsindikator_unauffaellig),
    Regel(
        "R005",
        "Kleiner Querschnitt bei großer Länge",
        _r005_kleiner_querschnitt_bei_grosser_laenge,
    ),
    Regel("R006", "Betonklasse vorhanden", _r006_betonklasse_vorhanden),
    Regel("R007", "Expositionsklasse vorhanden", _r007_expositionsklasse_vorhanden),
    Regel("R008", "Konstruktive Führbarkeit grob plausibel", _r008_konstruktive_fuehrbarkeit),
]
