from __future__ import annotations

from enum import Enum
from typing import Optional

from positionsplanung.model.bauteilposition import BauteilPosition


class Status(str, Enum):
    OK = "OK"
    WARNUNG = "WARNUNG"
    NICHT_ERFUELLT = "NICHT_ERFUELLT"
    NICHT_BEWERTET = "NICHT_BEWERTET"


class Stuetze:
    def __init__(
        self,
        position: BauteilPosition,
        breite_mm: float,
        hoehe_mm: float,
        laenge_mm: float,
        betonklasse: str | None = None,
        expositionsklasse: str | None = None,
        umgebung: str | None = None,
    ) -> None:
        self.position = position
        self.breite_mm = breite_mm
        self.hoehe_mm = hoehe_mm
        self.laenge_mm = laenge_mm
        self.betonklasse = betonklasse
        self.expositionsklasse = expositionsklasse
        self.umgebung = umgebung

    @property
    def querschnittsflaeche_mm2(self) -> float:
        return self.breite_mm * self.hoehe_mm

    @property
    def kleinste_abmessung_mm(self) -> float:
        return min(self.breite_mm, self.hoehe_mm)

    @property
    def groesste_abmessung_mm(self) -> float:
        return max(self.breite_mm, self.hoehe_mm)

    @property
    def seitenverhaeltnis(self) -> float:
        if self.kleinste_abmessung_mm <= 0:
            return float("inf")
        return self.groesste_abmessung_mm / self.kleinste_abmessung_mm

    @property
    def schlankheitsindikator(self) -> float:
        if self.kleinste_abmessung_mm <= 0:
            return float("inf")
        return self.laenge_mm / self.kleinste_abmessung_mm

    def ist_geometrisch_gueltig(self) -> bool:
        return (
            self.breite_mm > 0
            and self.hoehe_mm > 0
            and self.laenge_mm > 0
        )


class RuleResult:
    def __init__(
        self,
        regel_id: str,
        titel: str,
        status: Status,
        meldung: str,
        empfehlung: str = "",
    ) -> None:
        self.regel_id = regel_id
        self.titel = titel
        self.status = status
        self.meldung = meldung
        self.empfehlung = empfehlung

    def as_dict(self) -> dict:
        return {
            "regel_id": self.regel_id,
            "titel": self.titel,
            "status": self.status.value,
            "meldung": self.meldung,
            "empfehlung": self.empfehlung,
        }


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


class ReportBuilder:
    def to_markdown(self, stuetze: Stuetze, ergebnisse: list[RuleResult]) -> str:
        teile = [
            self._bauteilblock(stuetze),
            self._kennwerteblock(stuetze),
            self._regelblock(ergebnisse),
            self._fazitblock(ergebnisse),
        ]
        return "\n\n".join(teile)

    def _bauteilblock(self, stuetze: Stuetze) -> str:
        zeilen = [
            "# Bauteil-Steckbrief",
            "",
            "## Bauteilangaben",
            "",
            f"- **Position:** {stuetze.position}",
            f"- **Bezeichnung:** {stuetze.bezeichnung}",
            f"- **Breite:** {stuetze.breite_mm:.0f} mm",
            f"- **Höhe:** {stuetze.hoehe_mm:.0f} mm",
            f"- **Länge:** {stuetze.laenge_mm:.0f} mm",
        ]

        if stuetze.betonklasse:
            zeilen.append(f"- **Betonklasse:** {stuetze.betonklasse}")
        if stuetze.expositionsklasse:
            zeilen.append(f"- **Expositionsklasse:** {stuetze.expositionsklasse}")
        if stuetze.umgebung:
            zeilen.append(f"- **Umgebung:** {stuetze.umgebung}")
        if stuetze.bemerkung:
            zeilen.append(f"- **Bemerkung:** {stuetze.bemerkung}")

        return "\n".join(zeilen)

    def _kennwerteblock(self, stuetze: Stuetze) -> str:
        return "\n".join([
            "## Kennwerte",
            "",
            "| Kennwert | Wert |",
            "|---|---:|",
            f"| Querschnittsfläche | {stuetze.querschnittsflaeche_mm2:.0f} mm² |",
            f"| Kleinste Abmessung | {stuetze.kleinste_abmessung_mm:.0f} mm |",
            f"| Seitenverhältnis | {stuetze.seitenverhaeltnis:.2f} |",
            f"| Schlankheitsindikator | {stuetze.schlankheitsindikator:.2f} |",
        ])

    def _regelblock(self, ergebnisse: list[RuleResult]) -> str:
        zeilen = [
            "## Regelprüfungen",
            "",
            "| Regel | Titel | Status | Meldung | Empfehlung |",
            "|---|---|---|---|---|",
        ]

        for erg in ergebnisse:
            zeilen.append(
                f"| {erg.regel_id} | {erg.titel} | {erg.status.value} | "
                f"{erg.meldung} | {erg.empfehlung} |"
            )

        return "\n".join(zeilen)

    def _fazitblock(self, ergebnisse: list[RuleResult]) -> str:
        fehler = sum(1 for e in ergebnisse if e.status == Status.NICHT_ERFUELLT)
        warnungen = sum(1 for e in ergebnisse if e.status == Status.WARNUNG)

        if fehler > 0:
            text = "Es liegen nicht erfüllte Grundanforderungen vor."
        elif warnungen > 0:
            text = "Die Stütze ist grundsätzlich auswertbar, zeigt aber prüfbedürftige Punkte."
        else:
            text = "Die Stütze wirkt in der vorliegenden Vorprüfung unauffällig."

        return "\n".join([
            "## Fazit",
            "",
            text,
        ])