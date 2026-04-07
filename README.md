# positionsplanung

Erste testbare Version für ein kleines, regelbasiertes Python-Paket zur Ermittlung von Expositionsklassen für Betonbauteile.

## Enthalten

- interaktive CLI
- Klasse `Betonbauteil` als Zustandsobjekt
- regelbasierte Ableitung von Expositionsklassen
- einfache Ermittlung der maßgebenden Mindestdruckfestigkeitsklasse
- einfache Ermittlung von `c_min,dur`
- Tests für Grundfälle

## Wichtiger Hinweis

Diese Version ist **nur ein MVP zum Testen der Architektur**.
Sie ist **kein vollständiges Normprogramm** und bildet nicht alle Randbedingungen aus EC2 / DIN EN 206 / Nationalem Anhang ab.
Insbesondere sind die Regeln zu `XF`, `XA`, `XM`, Nutzungsdauer, Anforderungsklasse, `c_nom`, Verbund, Vorhaltemaß und projektspezifischen Sonderfällen noch stark vereinfacht.

## Projektstruktur

```text
positionsplanung/
├─ pyproject.toml
├─ README.md
├─ src/
│  └─ positionsplanung/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ model.py
│     ├─ questionnaire.py
│     ├─ rules.py
│     ├─ durability.py
│     └─ report.py
└─ tests/
   └─ test_basic.py
```

## In VS Code / Codex starten

### Mit `uv`

```bash
uv venv
.venv\Scripts\activate
uv pip install -e .
uv pip install -e .[dev]
positionsplanung
```

### Mit normalem `pip`

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
python -m pip install -e .[dev]
positionsplanung
```

## Tests

```bash
pytest
```

## Beispielidee

- Bauteil: Decke
- Lage: außen
- Feuchte: wechselnd nass/trocken
- Frost: ja
- Tausalz: ja

Erwartung in dieser Testversion:
- `XC4`
- `XD3`
- `XF4`
- maßgebende Mindestdruckfestigkeitsklasse: `C35/45`
- `c_min,dur`: `40 mm`
