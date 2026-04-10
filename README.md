# positionsplanung

Dieses Projekt bildet den Kern einer Prüfung für eine rechteckige Stahlbetonstütze ab. Es erzeugt einen kompakten Steckbrief, berechnet Kennwerte und prüft geometrische sowie konstruktive Regeln.

## Architektur

- `src/positionsplanung/models.py`
  - `RechteckStuetzeEingabe`: Eingabemodell für die Stütze
  - `RegelErgebnis`: vereinheitlichtes Ergebnis einer Regelprüfung
  - `StuetzeAuswertung`: Gesamtobjekt der Auswertung inklusive Kennwerte
- `src/positionsplanung/config.py`
  - zentrale Schwellenwerte für die Regeln
- `src/positionsplanung/rules.py`
  - 8 Prüfregeln mit einheitlichem Statussystem
- `src/positionsplanung/checker.py`
  - zentrale Prüfroutine über alle Regeln
- `src/positionsplanung/report.py`
  - kompakter Textsteckbrief; später erweiterbar um PDF/DOCX

## Statussystem

Alle Regeln geben einen von vier Werten zurück:

- `OK`
- `WARNUNG`
- `NICHT_ERFUELLT`
- `NICHT_BEWERTET`

## Nutzung im Notebook

```python
from positionsplanung.models import RechteckStuetzeEingabe
from positionsplanung.checker import pruefe_stuetze
from positionsplanung.report import erstelle_steckbrief

stuetze = RechteckStuetzeEingabe(
    position="A1",
    bezeichnung="Stütze 1",
    breite_mm=300,
    hoehe_mm=300,
    laenge_mm=4200,
    betonklasse="C30/37",
    expositionsklasse="XC1",
    umgebung="Innenbereich",
    bemerkung="Standardstütze",
)

auswertung = pruefe_stuetze(stuetze)
print(erstelle_steckbrief(auswertung))
print(auswertung.als_dataframe())
```

## Tests

```bash
pytest
```

## Annahmen

- Die Eingaben sind auf eine rechteckige Stahlbetonstütze beschränkt.
- Dimensionen werden in Millimetern angegeben.
- Der Schlankheitsindikator ist ein einfacher Vorprüfwert, kein normativer Nachweis.
- Schwellenwerte sind in `src/positionsplanung/config.py` zentral gespeichert.
