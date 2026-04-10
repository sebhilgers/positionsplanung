from positionsplanung import pruefe_stuetze, RechteckStuetzeEingabe, RegelStatus


def test_einfache_pruefung_als_integrationsfall():
    eingabe = RechteckStuetzeEingabe(
        position="C1",
        bezeichnung="Stütze Basis",
        breite_mm=250,
        hoehe_mm=250,
        laenge_mm=4500,
        betonklasse="C25/30",
        expositionsklasse="XC1",
    )

    auswertung = pruefe_stuetze(eingabe)
    assert len(auswertung.regelergebnisse) == 8
    assert all(ergebnis.status in (RegelStatus.OK, RegelStatus.WARNUNG, RegelStatus.NICHT_BEWERTET, RegelStatus.NICHT_ERFUELLT) for ergebnis in auswertung.regelergebnisse)
    assert auswertung.kennwerte["querschnittsflaeche_mm2"] == 62500.0
