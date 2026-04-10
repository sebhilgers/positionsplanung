from __future__ import annotations

import pandas as pd


class Expositionsklassen:
    """
    Modellierung von Expositionsklassen nach DIN EN 206 / EC2.

    Attribute:
        X0 : keine Bewehrungskorrosion
        XC, XD, XS : Korrosionsklassen (1–4 bzw. 1–3)
        XF : Frostangriff (1–4)
        XM : mechanischer Angriff (1–3)
        XA : chemischer Angriff (1–3)
        feuchteklasse : 'WO', 'WF' oder 'WA'
    """

    ERLAUBTE_FEUCHTE = {"WO", "WF", "WA"}

    def __init__(
        self,
        X0: bool = False,
        XC: int | None = None,
        XD: int | None = None,
        XS: int | None = None,
        XF: int | None = None,
        XM: int | None = None,
        XA: int | None = None,
        feuchteklasse: str | None = None,
    ):
        self.X0 = X0
        self.XC = XC
        self.XD = XD
        self.XS = XS
        self.XF = XF
        self.XM = XM
        self.XA = XA
        self.feuchteklasse = feuchteklasse

        self._validate()

    # =========================
    # Konstruktor-Helfer
    # =========================

    @classmethod
    def from_list(cls, klassen: list[str]) -> "Expositionsklassen":
        """
        Beispiel:
            ["XC3", "XF1", "XA2", "WF"]
        """
        kwargs = {
            "X0": False,
            "XC": None,
            "XD": None,
            "XS": None,
            "XF": None,
            "XM": None,
            "XA": None,
            "feuchteklasse": None,
        }

        for k in klassen:
            k = k.strip().upper()

            if k == "X0":
                kwargs["X0"] = True

            elif k.startswith("XC"):
                kwargs["XC"] = int(k[2:])

            elif k.startswith("XD"):
                kwargs["XD"] = int(k[2:])

            elif k.startswith("XS"):
                kwargs["XS"] = int(k[2:])

            elif k.startswith("XF"):
                kwargs["XF"] = int(k[2:])

            elif k.startswith("XM"):
                kwargs["XM"] = int(k[2:])

            elif k.startswith("XA"):
                kwargs["XA"] = int(k[2:])

            elif k in cls.ERLAUBTE_FEUCHTE:
                kwargs["feuchteklasse"] = k

            else:
                raise ValueError(f"Unbekannte Expositionsklasse: {k}")

        return cls(**kwargs)

    # =========================
    # Validierung
    # =========================

    def _validate(self) -> None:
        self._validate_range("XC", self.XC, 1, 4)
        self._validate_range("XD", self.XD, 1, 3)
        self._validate_range("XS", self.XS, 1, 3)
        self._validate_range("XF", self.XF, 1, 4)
        self._validate_range("XM", self.XM, 1, 3)
        self._validate_range("XA", self.XA, 1, 3)

        # X0 schließt Korrosion aus
        if self.X0 and any(v is not None for v in (self.XC, self.XD, self.XS)):
            raise ValueError("X0 schließt XC, XD und XS aus.")

        # Feuchteklasse prüfen
        if self.feuchteklasse is not None:
            if self.feuchteklasse not in self.ERLAUBTE_FEUCHTE:
                raise ValueError(
                    f"feuchteklasse muss eine von {self.ERLAUBTE_FEUCHTE} sein."
                )

    @staticmethod
    def _validate_range(name, value, min_v, max_v):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(f"{name} muss int oder None sein.")
        if not (min_v <= value <= max_v):
            raise ValueError(f"{name} muss zwischen {min_v} und {max_v} liegen.")

    # =========================
    # Zugriff / Darstellung
    # =========================

    def aktive_klassen(self) -> list[str]:
        """Gibt alle gesetzten Klassen als Liste zurück."""
        result = []

        if self.X0:
            result.append("X0")

        for name in ("XC", "XD", "XS", "XF", "XM", "XA"):
            value = getattr(self, name)
            if value is not None:
                result.append(f"{name}{value}")

        if self.feuchteklasse:
            result.append(self.feuchteklasse)

        return result

    def to_dict(self) -> dict:
        return {
            "X0": self.X0,
            "XC": self.XC,
            "XD": self.XD,
            "XS": self.XS,
            "XF": self.XF,
            "XM": self.XM,
            "XA": self.XA,
            "feuchteklasse": self.feuchteklasse,
        }

    def to_series(self) -> pd.Series:
        return pd.Series(self.to_dict())

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame([self.to_dict()])

    def __repr__(self) -> str:
        return f"Expositionsklassen({', '.join(self.aktive_klassen())})"