from __future__ import annotations

import pandas as pd
from IPython.display import Markdown, display


class CheckResult:
    def __init__(
        self,
        name: str,
        ok: bool,
        wert: float | None,
        grenzwert: float | None,
        einheit: str,
        meldung: str,
    ) -> None:
        self.name = name
        self.ok = ok
        self.wert = wert
        self.grenzwert = grenzwert
        self.einheit = einheit
        self.meldung = meldung

    @property
    def status(self) -> str:
        return "OK" if self.ok else "NICHT OK"

    def as_dict(self) -> dict:
        return {
            "Check": self.name,
            "Status": self.status,
            "Wert": self.wert,
            "Grenzwert": self.grenzwert,
            "Einheit": self.einheit,
            "Meldung": self.meldung,
        }

    def __repr__(self) -> str:
        return f"{self.name}: {self.status} – {self.meldung}"


class Stahlbetonstuetze:
    def __init__(
        self,
        b_mm: float,
        h_mm: float,
        l_mm: float,
        as_vorh_cm2: float | None = None,
        betonklasse: str | None = None,
    ) -> None:
        self.b_mm = b_mm
        self.h_mm = h_mm
        self.l_mm = l_mm
        self.as_vorh_cm2 = as_vorh_cm2
        self.betonklasse = betonklasse

        # pragmatische Standardwerte
        self.mindestabmessung_mm = 200.0
        self.asmin_faktor = 0.002
        self.asmax_faktor = 0.040

    @property
    def b_mm(self) -> float:
        return self._b_mm

    @b_mm.setter
    def b_mm(self, value: float) -> None:
        if value <= 0:
            raise ValueError("b_mm muss > 0 sein.")
        self._b_mm = float(value)

    @property
    def h_mm(self) -> float:
        return self._h_mm

    @h_mm.setter
    def h_mm(self, value: float) -> None:
        if value <= 0:
            raise ValueError("h_mm muss > 0 sein.")
        self._h_mm = float(value)

    @property
    def l_mm(self) -> float:
        return self._l_mm

    @l_mm.setter
    def l_mm(self, value: float) -> None:
        if value <= 0:
            raise ValueError("l_mm muss > 0 sein.")
        self._l_mm = float(value)

    @property
    def as_vorh_cm2(self) -> float | None:
        return self._as_vorh_cm2

    @as_vorh_cm2.setter
    def as_vorh_cm2(self, value: float | None) -> None:
        if value is None:
            self._as_vorh_cm2 = None
            return
        if value < 0:
            raise ValueError("as_vorh_cm2 darf nicht negativ sein.")
        self._as_vorh_cm2 = float(value)

    @property
    def a_mm2(self) -> float:
        return self.b_mm * self.h_mm

    @property
    def a_cm2(self) -> float:
        return self.a_mm2 / 100.0

    @property
    def kleinste_abmessung_mm(self) -> float:
        return min(self.b_mm, self.h_mm)

    @property
    def groesste_abmessung_mm(self) -> float:
        return max(self.b_mm, self.h_mm)

    @property
    def seitenverhaeltnis(self) -> float:
        return self.groesste_abmessung_mm / self.kleinste_abmessung_mm

    @property
    def schlankheitsindikator(self) -> float:
        return self.l_mm / self.kleinste_abmessung_mm

    @property
    def asmin_cm2(self) -> float:
        return self.asmin_faktor * self.a_cm2

    @property
    def asmax_cm2(self) -> float:
        return self.asmax_faktor * self.a_cm2

    @property
    def check_mindestabmessung(self) -> CheckResult:
        wert = self.kleinste_abmessung_mm
        grenzwert = self.mindestabmessung_mm
        ok = wert >= grenzwert

        if ok:
            meldung = f"Kleinste Abmessung {wert:.0f} mm ≥ {grenzwert:.0f} mm."
        else:
            meldung = f"Kleinste Abmessung {wert:.0f} mm < {grenzwert:.0f} mm."

        return CheckResult(
            name="Mindestabmessung",
            ok=ok,
            wert=wert,
            grenzwert=grenzwert,
            einheit="mm",
            meldung=meldung,
        )

    @property
    def check_asmin(self) -> CheckResult:
        if self.as_vorh_cm2 is None:
            return CheckResult(
                name="Mindestbewehrung As,min",
                ok=False,
                wert=None,
                grenzwert=self.asmin_cm2,
                einheit="cm²",
                meldung="As,vorh nicht angegeben.",
            )

        wert = self.as_vorh_cm2
        grenzwert = self.asmin_cm2
        ok = wert >= grenzwert

        if ok:
            meldung = f"As,vorh = {wert:.2f} cm² ≥ As,min = {grenzwert:.2f} cm²."
        else:
            meldung = f"As,vorh = {wert:.2f} cm² < As,min = {grenzwert:.2f} cm²."

        return CheckResult(
            name="Mindestbewehrung As,min",
            ok=ok,
            wert=wert,
            grenzwert=grenzwert,
            einheit="cm²",
            meldung=meldung,
        )

    @property
    def check_asmax(self) -> CheckResult:
        if self.as_vorh_cm2 is None:
            return CheckResult(
                name="Maximalbewehrung As,max",
                ok=False,
                wert=None,
                grenzwert=self.asmax_cm2,
                einheit="cm²",
                meldung="As,vorh nicht angegeben.",
            )

        wert = self.as_vorh_cm2
        grenzwert = self.asmax_cm2
        ok = wert <= grenzwert

        if ok:
            meldung = f"As,vorh = {wert:.2f} cm² ≤ As,max = {grenzwert:.2f} cm²."
        else:
            meldung = f"As,vorh = {wert:.2f} cm² > As,max = {grenzwert:.2f} cm²."

        return CheckResult(
            name="Maximalbewehrung As,max",
            ok=ok,
            wert=wert,
            grenzwert=grenzwert,
            einheit="cm²",
            meldung=meldung,
        )

    @property
    def checks(self) -> list[CheckResult]:
        return [
            self.check_mindestabmessung,
            self.check_asmin,
            self.check_asmax,
        ]

    @property
    def checks_df(self) -> pd.DataFrame:
        df = pd.DataFrame([check.as_dict() for check in self.checks])

        for spalte in ["Wert", "Grenzwert"]:
            df[spalte] = df[spalte].map(
                lambda x: round(x, 2) if isinstance(x, (int, float)) else x
            )

        return df

    @property
    def kennwerte_df(self) -> pd.DataFrame:
        daten = [
            {"Kennwert": "Breite b", "Wert": self.b_mm, "Einheit": "mm"},
            {"Kennwert": "Höhe h", "Wert": self.h_mm, "Einheit": "mm"},
            {"Kennwert": "Länge l", "Wert": self.l_mm, "Einheit": "mm"},
            {"Kennwert": "Querschnittsfläche A", "Wert": round(self.a_cm2, 2), "Einheit": "cm²"},
            {"Kennwert": "Kleinste Abmessung", "Wert": self.kleinste_abmessung_mm, "Einheit": "mm"},
            {"Kennwert": "Seitenverhältnis", "Wert": round(self.seitenverhaeltnis, 2), "Einheit": "-"},
            {"Kennwert": "Schlankheitsindikator", "Wert": round(self.schlankheitsindikator, 2), "Einheit": "-"},
            {"Kennwert": "As,min", "Wert": round(self.asmin_cm2, 2), "Einheit": "cm²"},
            {"Kennwert": "As,max", "Wert": round(self.asmax_cm2, 2), "Einheit": "cm²"},
        ]

        if self.as_vorh_cm2 is not None:
            daten.append(
                {"Kennwert": "As,vorh", "Wert": round(self.as_vorh_cm2, 2), "Einheit": "cm²"}
            )

        return pd.DataFrame(daten)
    
    def steckbrief_markdown(self) -> str:
        def df_to_md(df):
            return df.to_markdown(index=False)

        teile = []

        # Titel
        teile.append("# Bauteil-Steckbrief")
        teile.append("")

        # Bauteilangaben
        teile.append("## Bauteilangaben")
        teile.append("")
        teile.append(f"- Breite b = {self.b_mm:.0f} mm")
        teile.append(f"- Höhe h = {self.h_mm:.0f} mm")
        teile.append(f"- Länge l = {self.l_mm:.0f} mm")

        if self.betonklasse:
            teile.append(f"- Betonklasse = {self.betonklasse}")

        teile.append("")

        # Kennwerte
        teile.append("## Kennwerte")
        teile.append("")
        teile.append(df_to_md(self.kennwerte_df))
        teile.append("")

        # Checks
        teile.append("## Prüfungen")
        teile.append("")
        teile.append(df_to_md(self.checks_df))
        teile.append("")

        # Fazit
        n_ok = sum(1 for c in self.checks if c.ok)
        n_total = len(self.checks)

        if n_ok == n_total:
            fazit = "Alle geprüften Kriterien sind erfüllt."
        elif n_ok >= n_total / 2:
            fazit = "Einige Kriterien sind nicht erfüllt. Überprüfung empfohlen."
        else:
            fazit = "Mehrere Kriterien sind nicht erfüllt. Überarbeitung erforderlich."

        teile.append("## Fazit")
        teile.append("")
        teile.append(fazit)

        return "\n".join(teile)