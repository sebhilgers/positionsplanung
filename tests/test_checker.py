from positionsplanung.checker import pruefe_stuetze
from positionsplanung.models import RegelStatus, RechteckStuetzeEingabe
from positionsplanung.report import erstelle_steckbrief


def test_komplette_pruefung_normal():
    eingabe = RechteckStuetzeEingabe(
        position="B1",
        bezeichnung="Stütze Normal",
        breite_mm=300,
        hoehe_mm=300,
        laenge_mm=4200,
        betonklasse="C25/30",
        expositionsklasse="XC1",
        umgebung="Innenbereich",
    )

    auswertung = pruefe_stuetze(eingabe)
    assert len(auswertung.regelergebnisse) == 8
    assert any(ergebnis.status == RegelStatus.WARNUNG for ergebnis in auswertung.regelergebnisse)

    df = auswertung.als_dataframe()
    assert df.loc[df["regel_id"] == "R001", "status"].iloc[0] == RegelStatus.OK

    text = erstelle_steckbrief(auswertung)
    assert "Stütze Normal" in text
    assert "Kennwerte" in text


def test_komplette_pruefung_kritisch():
    eingabe = RechteckStuetzeEingabe(
        position="B2",
        bezeichnung="Stütze Kritisch",
        breite_mm=210,
        hoehe_mm=210,
        laenge_mm=6500,
    )

    auswertung = pruefe_stuetze(eingabe)
    status_uebersicht = auswertung.status_uebersicht()

    assert status_uebersicht[RegelStatus.OK] == 3
    assert status_uebersicht[RegelStatus.WARNUNG] >= 2
    assert status_uebersicht[RegelStatus.NICHT_BEWERTET] == 2
