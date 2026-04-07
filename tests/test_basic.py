from positionsplanung.model import Betonbauteil
from positionsplanung.rules import Expositionsbewerter
from positionsplanung.durability import Dauerhaftigkeitsbewerter


def test_innen_trocken_gibt_xc1():
    bauteil = Betonbauteil("Wand")
    bauteil.setze_parameter(
        lage="innen",
        feuchte="trocken",
        frost=False,
        tausalz=False,
        meerwasser=False,
        chemischer_angriff=None,
        verschleiss=None,
    )

    Expositionsbewerter().bewerte(bauteil)
    Dauerhaftigkeitsbewerter().bewerte(bauteil)

    assert bauteil.expositionsklassen == ["XC1"]
    assert bauteil.mindestfestigkeitsklasse == "C16/20"
    assert bauteil.cmin_dur_mm == 10


def test_aussen_tausalz_und_frost_gibt_xc4_xd3_xf4():
    bauteil = Betonbauteil("Decke")
    bauteil.setze_parameter(
        lage="aussen",
        feuchte="wechselnd_nass_trocken",
        frost=True,
        tausalz=True,
        meerwasser=False,
        chemischer_angriff=None,
        verschleiss=None,
    )

    Expositionsbewerter().bewerte(bauteil)
    Dauerhaftigkeitsbewerter().bewerte(bauteil)

    assert bauteil.expositionsklassen == ["XC4", "XD3", "XF4"]
    assert bauteil.mindestfestigkeitsklasse == "C35/45"
    assert bauteil.cmin_dur_mm == 40


def test_chemischer_angriff_wird_uebernommen():
    bauteil = Betonbauteil("Bodenplatte")
    bauteil.setze_parameter(
        lage="erdberuehrt",
        feuchte="dauerhaft_nass",
        frost=False,
        tausalz=False,
        meerwasser=False,
        chemischer_angriff="XA2",
        verschleiss=None,
    )

    Expositionsbewerter().bewerte(bauteil)
    Dauerhaftigkeitsbewerter().bewerte(bauteil)

    assert "XA2" in bauteil.expositionsklassen
    assert bauteil.mindestfestigkeitsklasse == "C35/45"
