from positionsplanung.model import Betonbauteil


def build_report(bauteil: Betonbauteil) -> str:
    lines = []
    lines.append("Ergebnis Expositionsbewertung")
    lines.append("=" * 32)
    lines.append(f"Bauteiltyp: {bauteil.bauteiltyp}")
    lines.append(f"Flaeche: {bauteil.flaeche or '-'}")
    lines.append(f"Lage: {bauteil.lage or '-'}")
    lines.append(f"Feuchte: {bauteil.feuchte or '-'}")
    lines.append("")

    if bauteil.expositionsklassen:
        lines.append("Ermittelte Expositionsklassen: " + ", ".join(bauteil.expositionsklassen))
    else:
        lines.append("Es wurden keine Expositionsklassen ermittelt.")

    if bauteil.begruendungen:
        lines.append("")
        lines.append("Begruendung:")
        for grund in bauteil.begruendungen:
            lines.append(f"- {grund}")

    lines.append("")
    if bauteil.mindestfestigkeitsklasse:
        lines.append(
            "Massgebende Mindestdruckfestigkeitsklasse: "
            f"{bauteil.mindestfestigkeitsklasse}"
        )
    else:
        lines.append("Keine Mindestdruckfestigkeitsklasse ermittelt.")

    if bauteil.cmin_dur_mm is not None:
        lines.append(f"Mindestbetondeckung aus Dauerhaftigkeit c_min,dur: {bauteil.cmin_dur_mm} mm")
    else:
        lines.append("Keine Betondeckung aus Dauerhaftigkeit ermittelt.")

    lines.append("")
    lines.append("Hinweis: Diese Ausgabe ist eine vereinfachte Testversion und ersetzt keine fachliche Pruefung.")
    return "\n".join(lines)
