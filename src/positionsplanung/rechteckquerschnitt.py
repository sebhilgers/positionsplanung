"""Rechteckquerschnitt mit Berechnung von Querschnittskennwerten."""

from __future__ import annotations

import numbers
from typing import Optional


class Rechteckquerschnitt:
    """Rechteckiger Querschnitt mit Kennwertberechnung.
    
    Alle Eingaben und Ausgaben in cm und cm².
    """

    def __init__(self, b_cm: float, h_cm: float) -> None:
        """Initialisiere einen rechteckigen Querschnitt.
        
        Args:
            b_cm: Breite in cm.
            h_cm: Höhe in cm.
            
        Raises:
            TypeError: Falls die Werte keine Zahlen sind.
            ValueError: Falls die Werte nicht positiv sind.
        """
        self.b_cm = self._validate_positive_dimension(b_cm, "b_cm")
        self.h_cm = self._validate_positive_dimension(h_cm, "h_cm")

    @staticmethod
    def _validate_positive_dimension(value: float, name: str) -> float:
        """Validiere eine positive Längendimension."""
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            raise TypeError(f"{name} muss eine Zahl sein")
        result = float(value)
        if result <= 0:
            raise ValueError(f"{name} muss größer als 0 cm sein")
        return result

    @property
    def querschnittsflaeche_cm2(self) -> float:
        """Querschnittsfläche in cm²."""
        return self.b_cm * self.h_cm

    @property
    def kleinste_abmessung_cm(self) -> float:
        """Kleinste Abmessung (min(b, h)) in cm."""
        return min(self.b_cm, self.h_cm)

    @property
    def groesste_abmessung_cm(self) -> float:
        """Größte Abmessung (max(b, h)) in cm."""
        return max(self.b_cm, self.h_cm)

    @property
    def seitenverhaeltnis(self) -> float:
        """Seitenverhältnis: max(b, h) / min(b, h)."""
        return self.groesste_abmessung_cm / self.kleinste_abmessung_cm

    @property
    def umfang_cm(self) -> float:
        """Umfang in cm."""
        return 2 * (self.b_cm + self.h_cm)

    @property
    def diagonal_cm(self) -> float:
        """Diagonale in cm."""
        return (self.b_cm**2 + self.h_cm**2) ** 0.5

    @property
    def traegheitsmoment_y_cm4(self) -> float:
        """Trägheitsmoment um die y-Achse (bezogen auf Breite b).
        
        Iy = b * h³ / 12
        """
        return (self.b_cm * self.h_cm**3) / 12

    @property
    def traegheitsmoment_z_cm4(self) -> float:
        """Trägheitsmoment um die z-Achse (bezogen auf Höhe h).
        
        Iz = h * b³ / 12
        """
        return (self.h_cm * self.b_cm**3) / 12

    @property
    def widerstandsmoment_y_cm3(self) -> float:
        """Widerstandsmoment um die y-Achse.
        
        Wy = Iy / (h/2) = b * h² / 6
        """
        return (self.b_cm * self.h_cm**2) / 6

    @property
    def widerstandsmoment_z_cm3(self) -> float:
        """Widerstandsmoment um die z-Achse.
        
        Wz = Iz / (b/2) = h * b² / 6
        """
        return (self.h_cm * self.b_cm**2) / 6

    @property
    def traegheitsradius_y_cm(self) -> float:
        """Trägheitsradius um die y-Achse: iy = sqrt(Iy / A)."""
        return (self.traegheitsmoment_y_cm4 / self.querschnittsflaeche_cm2) ** 0.5

    @property
    def traegheitsradius_z_cm(self) -> float:
        """Trägheitsradius um die z-Achse: iz = sqrt(Iz / A)."""
        return (self.traegheitsmoment_z_cm4 / self.querschnittsflaeche_cm2) ** 0.5

    @property
    def traegheitsradius_min_cm(self) -> float:
        """Minimaler Trägheitsradius."""
        return min(self.traegheitsradius_y_cm, self.traegheitsradius_z_cm)

    def als_dict(self) -> dict[str, float]:
        """Gebe alle Kennwerte als Dictionary zurück."""
        return {
            "b_cm": self.b_cm,
            "h_cm": self.h_cm,
            "querschnittsflaeche_cm2": self.querschnittsflaeche_cm2,
            "kleinste_abmessung_cm": self.kleinste_abmessung_cm,
            "groesste_abmessung_cm": self.groesste_abmessung_cm,
            "seitenverhaeltnis": self.seitenverhaeltnis,
            "umfang_cm": self.umfang_cm,
            "diagonal_cm": self.diagonal_cm,
            "traegheitsmoment_y_cm4": self.traegheitsmoment_y_cm4,
            "traegheitsmoment_z_cm4": self.traegheitsmoment_z_cm4,
            "widerstandsmoment_y_cm3": self.widerstandsmoment_y_cm3,
            "widerstandsmoment_z_cm3": self.widerstandsmoment_z_cm3,
            "traegheitsradius_y_cm": self.traegheitsradius_y_cm,
            "traegheitsradius_z_cm": self.traegheitsradius_z_cm,
            "traegheitsradius_min_cm": self.traegheitsradius_min_cm,
        }

    def __repr__(self) -> str:
        """String-Darstellung."""
        return (
            f"Rechteckquerschnitt(b={self.b_cm} cm, h={self.h_cm} cm, "
            f"A={self.querschnittsflaeche_cm2:.2f} cm²)"
        )
