# check_stahlbetonstuetze.py

from positionsplanung.regelpruefung.checks import Status, RuleResult
from positionsplanung.konstruktionsregeln.stahlbetonstuetze import Stuetze

class Regelpruefer:
    def __init__(
        self,
        mindestabmessung_mm: float = 250.0,
        max_seitenverhaeltnis: float = 4.0,
        max_schlankheitsindikator: float = 15.0,
        kleine_abmessung_mm: float = 240.0,
        grosse_laenge_mm: float = 3500.0,
        kritische_fuehrbarkeit_mm: float = 220.0,
    ) -> None:
        self.mindestabmessung_mm = mindestabmessung_mm
        self.max_seitenverhaeltnis = max_seitenverhaeltnis
        self.max_schlankheitsindikator = max_schlankheitsindikator
        self.kleine_abmessung_mm = kleine_abmessung_mm
        self.grosse_laenge_mm = grosse_laenge_mm
        self.kritische_fuehrbarkeit_mm = kritische_fuehrbarkeit_mm

    def pruefe(self, stuetze: Stuetze) -> list[RuleResult]:
        ergebnisse: list[RuleResult] = []

        ergebnisse.append(self._pruefe_grundwerte(stuetze))
        ergebnisse.append(self._pruefe_mindestabmessung(stuetze))
        ergebnisse.append(self._pruefe_seitenverhaeltnis(stuetze))
        ergebnisse.append(self._pruefe_schlankheit(stuetze))
        ergebnisse.append(self._pruefe_kleiner_querschnitt_und_laenge(stuetze))
        ergebnisse.append(self._pruefe_betonklasse(stuetze))
        ergebnisse.append(self._pruefe_expositionsklasse(stuetze))
        ergebnisse.append(self._pruefe_fuehrbarkeit(stuetze))

        return ergebnisse

    def _pruefe_grundwerte(self, stuetze: Stuetze) -> RuleResult:
        if stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R001",
                "Grundwerte positiv",
                Status.OK,
                "Alle geometrischen Grundwerte sind positiv.",
            )
        return RuleResult(
            "R001",
            "Grundwerte positiv",
            Status.NICHT_ERFUELLT,
            "Mindestens ein geometrischer Grundwert ist nicht positiv.",
            "Breite, Höhe und Länge prüfen.",
        )

    def _pruefe_mindestabmessung(self, stuetze: Stuetze) -> RuleResult:
        if not stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R002",
                "Mindestabmessung eingehalten",
                Status.NICHT_BEWERTET,
                "Die Regel kann wegen ungültiger Geometrie nicht bewertet werden.",
            )

        if stuetze.kleinste_abmessung_mm >= self.mindestabmessung_mm:
            return RuleResult(
                "R002",
                "Mindestabmessung eingehalten",
                Status.OK,
                f"Die kleinste Abmessung beträgt {stuetze.kleinste_abmessung_mm:.0f} mm.",
            )
        return RuleResult(
            "R002",
            "Mindestabmessung eingehalten",
            Status.WARNUNG,
            f"Die kleinste Abmessung beträgt nur {stuetze.kleinste_abmessung_mm:.0f} mm.",
            "Querschnitt in der kleineren Richtung prüfen.",
        )

    def _pruefe_seitenverhaeltnis(self, stuetze: Stuetze) -> RuleResult:
        if not stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R003",
                "Seitenverhältnis unauffällig",
                Status.NICHT_BEWERTET,
                "Die Regel kann wegen ungültiger Geometrie nicht bewertet werden.",
            )

        if stuetze.seitenverhaeltnis <= self.max_seitenverhaeltnis:
            return RuleResult(
                "R003",
                "Seitenverhältnis unauffällig",
                Status.OK,
                f"Das Seitenverhältnis beträgt {stuetze.seitenverhaeltnis:.2f}.",
            )
        return RuleResult(
            "R003",
            "Seitenverhältnis unauffällig",
            Status.WARNUNG,
            f"Das Seitenverhältnis beträgt {stuetze.seitenverhaeltnis:.2f} und ist erhöht.",
            "Querschnittsproportionen prüfen.",
        )

    def _pruefe_schlankheit(self, stuetze: Stuetze) -> RuleResult:
        if not stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R004",
                "Schlankheitsindikator unauffällig",
                Status.NICHT_BEWERTET,
                "Die Regel kann wegen ungültiger Geometrie nicht bewertet werden.",
            )

        if stuetze.schlankheitsindikator <= self.max_schlankheitsindikator:
            return RuleResult(
                "R004",
                "Schlankheitsindikator unauffällig",
                Status.OK,
                f"Der Schlankheitsindikator beträgt {stuetze.schlankheitsindikator:.2f}.",
            )
        return RuleResult(
            "R004",
            "Schlankheitsindikator unauffällig",
            Status.WARNUNG,
            f"Der Schlankheitsindikator beträgt {stuetze.schlankheitsindikator:.2f} und ist erhöht.",
            "Abmessungen und Systemannahmen vertieft prüfen.",
        )

    def _pruefe_kleiner_querschnitt_und_laenge(self, stuetze: Stuetze) -> RuleResult:
        if not stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R005",
                "Kleiner Querschnitt bei großer Länge",
                Status.NICHT_BEWERTET,
                "Die Regel kann wegen ungültiger Geometrie nicht bewertet werden.",
            )

        kritisch = (
            stuetze.kleinste_abmessung_mm < self.kleine_abmessung_mm
            and stuetze.laenge_mm > self.grosse_laenge_mm
        )

        if kritisch:
            return RuleResult(
                "R005",
                "Kleiner Querschnitt bei großer Länge",
                Status.WARNUNG,
                "Die Kombination aus kleiner Abmessung und großer Länge ist auffällig.",
                "Geometrie und Tragkonzept prüfen.",
            )
        return RuleResult(
            "R005",
            "Kleiner Querschnitt bei großer Länge",
            Status.OK,
            "Die Kombination aus Abmessung und Länge ist unauffällig.",
        )

    def _pruefe_betonklasse(self, stuetze: Stuetze) -> RuleResult:
        if stuetze.betonklasse and stuetze.betonklasse.strip():
            return RuleResult(
                "R006",
                "Betonklasse vorhanden",
                Status.OK,
                f"Betonklasse angegeben: {stuetze.betonklasse}.",
            )
        return RuleResult(
            "R006",
            "Betonklasse vorhanden",
            Status.NICHT_BEWERTET,
            "Es wurde keine Betonklasse angegeben.",
            "Materialangaben ergänzen.",
        )

    def _pruefe_expositionsklasse(self, stuetze: Stuetze) -> RuleResult:
        if stuetze.expositionsklasse and stuetze.expositionsklasse.strip():
            return RuleResult(
                "R007",
                "Expositionsklasse vorhanden",
                Status.OK,
                f"Expositionsklasse angegeben: {stuetze.expositionsklasse}.",
            )
        return RuleResult(
            "R007",
            "Expositionsklasse vorhanden",
            Status.NICHT_BEWERTET,
            "Es wurde keine Expositionsklasse angegeben.",
            "Expositionsklasse ergänzen.",
        )

    def _pruefe_fuehrbarkeit(self, stuetze: Stuetze) -> RuleResult:
        if not stuetze.ist_geometrisch_gueltig():
            return RuleResult(
                "R008",
                "Konstruktive Führbarkeit grob plausibel",
                Status.NICHT_BEWERTET,
                "Die Regel kann wegen ungültiger Geometrie nicht bewertet werden.",
            )

        if stuetze.kleinste_abmessung_mm < self.kritische_fuehrbarkeit_mm:
            return RuleResult(
                "R008",
                "Konstruktive Führbarkeit grob plausibel",
                Status.WARNUNG,
                "Die kleinste Abmessung ist sehr gering.",
                "Bewehrungsführung und Knotenausbildung kritisch prüfen.",
            )
        return RuleResult(
            "R008",
            "Konstruktive Führbarkeit grob plausibel",
            Status.OK,
            "Die Abmessungen wirken hinsichtlich der groben Führbarkeit unauffällig.",
        )