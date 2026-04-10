import pytest

from positionsplanung.config import (
    FUEHRBARKEIT_KLEINSTE_ABMESSUNG_MM,
    KLEINE_QUERSCHNITT_LAENGE_MM,
    KLEINE_QUERSCHNITT_MINDSTABMESSUNG_MM,
    MINDESTABMESSUNG_MM,
    SCHLANKHEITSINDIKATOR_WARNUNG,
    SEITENVERHAELTNIS_WARNUNG,
)
from positionsplanung.models import RegelStatus, RechteckStuetzeEingabe
from positionsplanung.rules import ALLE_REGELN


def _finde_regel(regel_id: str):
    return next((regel for regel in ALLE_REGELN if regel.regel_id == regel_id), None)


def test_r001_grundwerte_positiv_erfolgreich():
    eingabe = RechteckStuetzeEingabe(
        position="A1",
        bezeichnung="Stütze 1",
        breite_mm=300,
        hoehe_mm=400,
        laenge_mm=3600,
        betonklasse="C30/37",
        expositionsklasse="XC1",
    )

    regel = _finde_regel("R001")
    assert regel is not None
    ergebnis = regel.pruefe(eingabe)

    assert ergebnis.status == RegelStatus.OK
    assert "größer als 0" not in ergebnis.meldung


def test_r002_mindestabmessung_nicht_erfuellt():
    eingabe = RechteckStuetzeEingabe(
        position="A2",
        bezeichnung="Stütze 2",
        breite_mm=180,
        hoehe_mm=220,
        laenge_mm=3500,
    )

    regel = _finde_regel("R002")
    assert regel is not None
    ergebnis = regel.pruefe(eingabe)

    assert ergebnis.status == RegelStatus.NICHT_ERFUELLT
    assert "200 mm" in ergebnis.meldung


def test_r005_warnung_kleiner_querschnitt_grosse_laenge():
    eingabe = RechteckStuetzeEingabe(
        position="A3",
        bezeichnung="Stütze 3",
        breite_mm=240,
        hoehe_mm=240,
        laenge_mm=KLEINE_QUERSCHNITT_LAENGE_MM + 100,
    )

    regel = _finde_regel("R005")
    assert regel is not None
    ergebnis = regel.pruefe(eingabe)

    assert ergebnis.status == RegelStatus.WARNUNG
    assert "kleine Abmessung" in ergebnis.meldung


def test_r008_fuehrbarkeit_warnung():
    eingabe = RechteckStuetzeEingabe(
        position="A4",
        bezeichnung="Stütze 4",
        breite_mm=210,
        hoehe_mm=210,
        laenge_mm=4200,
    )

    regel = _finde_regel("R008")
    assert regel is not None
    ergebnis = regel.pruefe(eingabe)

    assert ergebnis.status == RegelStatus.WARNUNG
    assert "kritisch" in ergebnis.meldung
    assert "210.0 mm" in ergebnis.meldung
