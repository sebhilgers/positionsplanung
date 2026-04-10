from .models import RegelStatus, StuetzeAuswertung


def erstelle_steckbrief(auswertung: StuetzeAuswertung) -> str:
    if not isinstance(auswertung, StuetzeAuswertung):
        raise TypeError("Die Auswertung muss ein StuetzeAuswertung-Objekt sein")

    eingabe = auswertung.eingabe
    lines = [
        f"Stütze: {eingabe.bezeichnung} ({eingabe.position})",
        f"Betonklasse: {eingabe.betonklasse or 'nicht angegeben'}",
        f"Expositionsklasse: {eingabe.expositionsklasse or 'nicht angegeben'}",
        f"Umgebung: {eingabe.umgebung or 'nicht angegeben'}",
        f"Bemerkung: {eingabe.bemerkung or 'keine'}",
        "",
        "Kennwerte:",
        f"  Querschnittsfläche: {auswertung.kennwerte['querschnittsflaeche_mm2']:.1f} mm²",
        f"  Kleinste Abmessung: {auswertung.kennwerte['kleinste_abmessung_mm']:.1f} mm",
        f"  Seitenverhältnis: {auswertung.kennwerte['seitenverhaeltnis']:.2f}",
        f"  Schlankheitsindikator: {auswertung.kennwerte['schlankheitsindikator']:.2f}",
        "",
        "Regelübersicht:",
    ]

    for ergebnis in auswertung.regelergebnisse:
        status = ergebnis.status
        lines.append(f"  {ergebnis.regel_id}: {status} - {ergebnis.titel}")
        if status != RegelStatus.OK:
            lines.append(f"    Hinweis: {ergebnis.meldung}")
            if ergebnis.empfehlung:
                lines.append(f"    Empfehlung: {ergebnis.empfehlung}")

    return "\n".join(lines)
