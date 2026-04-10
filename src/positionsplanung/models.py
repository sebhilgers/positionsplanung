from __future__ import annotations

import numbers
from typing import Optional

import pandas as pd


class RegelStatus:
    OK = "OK"
    WARNUNG = "WARNUNG"
    NICHT_ERFUELLT = "NICHT_ERFUELLT"
    NICHT_BEWERTET = "NICHT_BEWERTET"

    @classmethod
    def alle(cls) -> tuple[str, ...]:
        return (cls.OK, cls.WARNUNG, cls.NICHT_ERFUELLT, cls.NICHT_BEWERTET)


class RegelErgebnis:
    def __init__(
        self,
        regel_id: str,
        titel: str,
        status: str,
        meldung: str,
        empfehlung: str,
    ) -> None:
        if status not in RegelStatus.alle():
            raise ValueError(f"Unbekannter Regelstatus: {status}")
        self.regel_id = regel_id
        self.titel = titel
        self.status = status
        self.meldung = meldung
        self.empfehlung = empfehlung

    def as_dict(self) -> dict[str, str]:
        return {
            "regel_id": self.regel_id,
            "titel": self.titel,
            "status": self.status,
            "meldung": self.meldung,
            "empfehlung": self.empfehlung,
        }


class RechteckStuetzeEingabe:
    def __init__(
        self,
        position: str,
        bezeichnung: str,
        breite_mm: float,
        hoehe_mm: float,
        laenge_mm: float,
        betonklasse: Optional[str] = None,
        expositionsklasse: Optional[str] = None,
        umgebung: Optional[str] = None,
        bemerkung: Optional[str] = None,
    ) -> None:
        self.position = self._validate_text(position, "position")
        self.bezeichnung = self._validate_text(bezeichnung, "bezeichnung")
        self.breite_mm = self._validate_positive_length(breite_mm, "breite_mm")
        self.hoehe_mm = self._validate_positive_length(hoehe_mm, "hoehe_mm")
        self.laenge_mm = self._validate_positive_length(laenge_mm, "laenge_mm")
        self.betonklasse = self._normalize_optional_text(betonklasse)
        self.expositionsklasse = self._normalize_optional_text(expositionsklasse)
        self.umgebung = self._normalize_optional_text(umgebung)
        self.bemerkung = self._normalize_optional_text(bemerkung)

    @staticmethod
    def _validate_text(value: str, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} muss ein Textwert sein")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{name} darf nicht leer sein")
        return normalized

    @staticmethod
    def _normalize_optional_text(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Optionale Textfelder müssen Text sein")
        normalized = value.strip()
        return normalized or None

    @staticmethod
    def _validate_positive_length(value: float, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            raise TypeError(f"{name} muss eine Zahl sein")
        result = float(value)
        if result <= 0:
            raise ValueError(f"{name} muss größer als 0 sein")
        return result

    @property
    def querschnittsflaeche_mm2(self) -> float:
        return self.breite_mm * self.hoehe_mm

    @property
    def kleinste_abmessung_mm(self) -> float:
        return min(self.breite_mm, self.hoehe_mm)

    @property
    def seitenverhaeltnis(self) -> float:
        return max(self.breite_mm, self.hoehe_mm) / self.kleinste_abmessung_mm

    @property
    def schlankheitsindikator(self) -> float:
        return self.laenge_mm / self.kleinste_abmessung_mm

    def als_dict(self) -> dict[str, Optional[str | float]]:
        return {
            "position": self.position,
            "bezeichnung": self.bezeichnung,
            "breite_mm": self.breite_mm,
            "hoehe_mm": self.hoehe_mm,
            "laenge_mm": self.laenge_mm,
            "betonklasse": self.betonklasse,
            "expositionsklasse": self.expositionsklasse,
            "umgebung": self.umgebung,
            "bemerkung": self.bemerkung,
        }


class StuetzeAuswertung:
    def __init__(self, eingabe: RechteckStuetzeEingabe, regelergebnisse: list[RegelErgebnis]) -> None:
        self.eingabe = eingabe
        self.regelergebnisse = list(regelergebnisse)

    @property
    def kennwerte(self) -> dict[str, float]:
        return {
            "querschnittsflaeche_mm2": self.eingabe.querschnittsflaeche_mm2,
            "kleinste_abmessung_mm": self.eingabe.kleinste_abmessung_mm,
            "seitenverhaeltnis": self.eingabe.seitenverhaeltnis,
            "schlankheitsindikator": self.eingabe.schlankheitsindikator,
        }

    def als_dataframe(self) -> pd.DataFrame:
        rows = [ergebnis.as_dict() for ergebnis in self.regelergebnisse]
        return pd.DataFrame(rows)

    def status_uebersicht(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for ergebnis in self.regelergebnisse:
            summary[ergebnis.status] = summary.get(ergebnis.status, 0) + 1
        return summary
