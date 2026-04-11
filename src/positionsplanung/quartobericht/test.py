class Stuetze:
    def __init__(
        self,
        position: str,
        bezeichnung: str,
        breite_mm: float,
        hoehe_mm: float,
        laenge_mm: float,
        betonklasse: str | None = None,
        expositionsklasse: str | None = None,
        umgebung: str | None = None,
        bemerkung: str | None = None,
    ) -> None:
        self.position = position
        self.bezeichnung = bezeichnung
        self.breite_mm = breite_mm
        self.hoehe_mm = hoehe_mm
        self.laenge_mm = laenge_mm
        self.betonklasse = betonklasse
        self.expositionsklasse = expositionsklasse
        self.umgebung = umgebung
        self.bemerkung = bemerkung


def berechne_kennwerte(stuetze: Stuetze) -> dict:
    kleinste_abmessung = min(stuetze.breite_mm, stuetze.hoehe_mm)
    groesste_abmessung = max(stuetze.breite_mm, stuetze.hoehe_mm)

    return {
        "querschnittsflaeche_mm2": stuetze.breite_mm * stuetze.hoehe_mm,
        "kleinste_abmessung_mm": kleinste_abmessung,
        "seitenverhaeltnis": groesste_abmessung / kleinste_abmessung,
        "schlankheitsindikator": stuetze.laenge_mm / kleinste_abmessung,
    }

def pruefe_regeln(stuetze: Stuetze, kennwerte: dict) -> list[dict]:
    ergebnisse: list[dict] = []

    if stuetze.breite_mm > 0 and stuetze.hoehe_mm > 0 and stuetze.laenge_mm > 0:
        ergebnisse.append({
            "regel_id": "R001",
            "titel": "Grundwerte positiv",
            "status": "OK",
            "meldung": "Alle geometrischen Grundwerte sind positiv.",
            "empfehlung": "",
        })
    else:
        ergebnisse.append({
            "regel_id": "R001",
            "titel": "Grundwerte positiv",
            "status": "NICHT_ERFUELLT",
            "meldung": "Mindestens ein geometrischer Grundwert ist nicht positiv.",
            "empfehlung": "Breite, Höhe und Länge prüfen.",
        })

    if kennwerte["kleinste_abmessung_mm"] < 250:
        ergebnisse.append({
            "regel_id": "R002",
            "titel": "Mindestabmessung",
            "status": "WARNUNG",
            "meldung": "Die kleinste Abmessung ist kleiner als 250 mm.",
            "empfehlung": "Querschnitt in der kleineren Richtung prüfen.",
        })
    else:
        ergebnisse.append({
            "regel_id": "R002",
            "titel": "Mindestabmessung",
            "status": "OK",
            "meldung": "Die kleinste Abmessung ist unauffällig.",
            "empfehlung": "",
        })

    if kennwerte["schlankheitsindikator"] > 15:
        ergebnisse.append({
            "regel_id": "R003",
            "titel": "Schlankheitsindikator",
            "status": "WARNUNG",
            "meldung": "Der einfache Schlankheitsindikator ist erhöht.",
            "empfehlung": "Stützenabmessungen und Systemannahmen vertieft prüfen.",
        })
    else:
        ergebnisse.append({
            "regel_id": "R003",
            "titel": "Schlankheitsindikator",
            "status": "OK",
            "meldung": "Der einfache Schlankheitsindikator ist unauffällig.",
            "empfehlung": "",
        })

    return ergebnisse

def render_bauteiluebersicht(stuetze: Stuetze) -> str:
    lines = [
        "# Bauteil-Steckbrief",
        "",
        "## Bauteilangaben",
        "",
        f"- **Position:** {stuetze.position}",
        f"- **Bezeichnung:** {stuetze.bezeichnung}",
        f"- **Abmessungen:** {stuetze.breite_mm:.0f} / {stuetze.hoehe_mm:.0f} / {stuetze.laenge_mm:.0f} mm",
    ]

    if stuetze.betonklasse:
        lines.append(f"- **Betonklasse:** {stuetze.betonklasse}")
    if stuetze.expositionsklasse:
        lines.append(f"- **Expositionsklasse:** {stuetze.expositionsklasse}")
    if stuetze.umgebung:
        lines.append(f"- **Umgebung:** {stuetze.umgebung}")
    if stuetze.bemerkung:
        lines.append(f"- **Bemerkung:** {stuetze.bemerkung}")

    return "\n".join(lines)

def render_kennwerte_markdown(kennwerte: dict) -> str:
    return "\n".join([
        "## Kennwerte",
        "",
        "| Kennwert | Wert |",
        "|---|---:|",
        f"| Querschnittsfläche | {kennwerte['querschnittsflaeche_mm2']:.0f} mm² |",
        f"| Kleinste Abmessung | {kennwerte['kleinste_abmessung_mm']:.0f} mm |",
        f"| Seitenverhältnis | {kennwerte['seitenverhaeltnis']:.2f} |",
        f"| Schlankheitsindikator | {kennwerte['schlankheitsindikator']:.2f} |",
    ])

def render_regeln_markdown(regeln: list[dict]) -> str:
    lines = [
        "## Regelprüfungen",
        "",
        "| Regel | Titel | Status | Meldung | Empfehlung |",
        "|---|---|---|---|---|",
    ]

    for regel in regeln:
        lines.append(
            f"| {regel['regel_id']} | {regel['titel']} | {regel['status']} | "
            f"{regel['meldung']} | {regel['empfehlung']} |"
        )

    return "\n".join(lines)

def render_fazit_markdown(regeln: list[dict]) -> str:
    anzahl_warnungen = sum(1 for r in regeln if r["status"] == "WARNUNG")
    anzahl_fehler = sum(1 for r in regeln if r["status"] == "NICHT_ERFUELLT")

    if anzahl_fehler > 0:
        text = "Das Bauteil weist kritische Eingaben oder nicht erfüllte Grundanforderungen auf."
    elif anzahl_warnungen > 0:
        text = "Das Bauteil ist grundsätzlich auswertbar, zeigt jedoch auffällige Punkte für die weitere Planung."
    else:
        text = "Das Bauteil wirkt in der vorliegenden Vorprüfung geometrisch unauffällig."

    return "\n".join([
        "## Fazit",
        "",
        text,
    ])