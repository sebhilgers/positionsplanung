"""Tests für die Rechteckquerschnitt-Klasse."""

import pytest

from positionsplanung.rechteckquerschnitt import Rechteckquerschnitt


def test_rechteckquerschnitt_grundlagen():
    """Teste Initialisierung und Grundkennwerte."""
    qn = Rechteckquerschnitt(b_mm=30, h_mm=40)
    
    assert qn.b_cm == 30.0
    assert qn.h_cm == 40.0
    assert qn.A_c_cm2 == 1200.0
    assert qn.kleinste_abmessung_cm == 30.0
    assert qn.groesste_abmessung_cm == 40.0
    assert abs(qn.seitenverhaeltnis - 40 / 30) < 0.001


def test_rechteckquerschnitt_traegheitsmomente():
    """Teste Trägheitsmomente und Widerstandsmomente."""
    qn = Rechteckquerschnitt(b_mm=20, h_mm=40)
    
    # Iy = b * h³ / 12 = 20 * 40³ / 12 = 20 * 64000 / 12 = 106666.67
    expected_iy = (20 * 40**3) / 12
    assert abs(qn.traegheitsmoment_y_cm4 - expected_iy) < 0.01
    
    # Wy = b * h² / 6 = 20 * 1600 / 6 = 5333.33
    expected_wy = (20 * 40**2) / 6
    assert abs(qn.widerstandsmoment_y_cm3 - expected_wy) < 0.01


def test_rechteckquerschnitt_diagonal():
    """Teste Diagonale."""
    qn = Rechteckquerschnitt(b_mm=3, h_mm=4)
    
    # 3-4-5 Dreieck
    assert abs(qn.diagonal_cm - 5.0) < 0.001


def test_rechteckquerschnitt_traegheitsradius():
    """Teste Trägheitsradius."""
    qn = Rechteckquerschnitt(b_mm=20, h_mm=40)
    
    # iy = sqrt(Iy / A)
    iy_expected = (qn.traegheitsmoment_y_cm4 / qn.A_c_cm2) ** 0.5
    assert abs(qn.traegheitsradius_y_cm - iy_expected) < 0.001


def test_rechteckquerschnitt_quadrat():
    """Teste Quadratquerschnitt."""
    qn = Rechteckquerschnitt(b_mm=30, h_mm=30)
    
    assert qn.A_c_cm2 == 900.0
    assert qn.seitenverhaeltnis == 1.0
    assert qn.traegheitsradius_y_cm == qn.traegheitsradius_z_cm


def test_rechteckquerschnitt_validation():
    """Teste Validierung."""
    with pytest.raises(ValueError):
        Rechteckquerschnitt(b_mm=-10, h_mm=30)
    
    with pytest.raises(ValueError):
        Rechteckquerschnitt(b_mm=20, h_mm=0)
    
    with pytest.raises(TypeError):
        Rechteckquerschnitt(b_mm="30", h_mm=40)


def test_rechteckquerschnitt_dict():
    """Teste Dictionary-Ausgabe."""
    qn = Rechteckquerschnitt(b_mm=25, h_mm=35)
    d = qn.to_dict()
    
    assert d["b_cm"] == 25.0
    assert d["h_cm"] == 35.0
    assert d["querschnittsflaeche_cm2"] == 875.0
    assert "traegheitsmoment_y_cm4" in d
    assert "widerstandsmoment_z_cm3" in d
