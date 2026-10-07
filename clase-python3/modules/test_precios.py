from math import isclose

from precios import precio_descuento


def test_descuento_del_10_por_ciento():
    assert isclose(precio_descuento(100, 0.1), 90)


def test_descuentos_habituales():
    for descuento, esperado in [(0.2, 80), (0.3, 70), (0.5, 50), (0.9, 10)]:
        assert isclose(precio_descuento(100, descuento), esperado)


def test_sin_descuento_devuelve_el_precio_original():
    assert precio_descuento(100, 0) == 100


def test_descuento_total_devuelve_cero():
    assert precio_descuento(100, 1) == 0


def test_precio_cero():
    assert precio_descuento(0, 0.5) == 0


def test_precio_decimal():
    assert isclose(precio_descuento(19.99, 0.25), 14.9925)
