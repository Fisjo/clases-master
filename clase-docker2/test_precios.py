import pytest
from hypothesis import given, strategies as st
from precios import precio_final

precios = st.floats(min_value=0, max_value=1e6)
descuentos = st.floats(min_value=0, max_value=100)


# --- Ejemplos concretos ---

@pytest.mark.parametrize("precio, descuento, esperado", [
    (100, 20, 80),
    (100, 0, 100),
    (100, 100, 0),
    (50, 10, 45),
    (0, 50, 0),
    (19.99, 10, 17.991),
])
def test_ejemplos(precio, descuento, esperado):
    assert precio_final(precio, descuento) == pytest.approx(esperado)


def test_descuento_por_defecto_es_cero():
    assert precio_final(50) == 50


# --- Propiedades generales ---

@given(precios, descuentos)
def test_resultado_entre_cero_y_precio_original(precio, descuento):
    assert 0 <= precio_final(precio, descuento) <= precio


@given(precios)
def test_sin_descuento_no_cambia(precio):
    assert precio_final(precio, 0) == precio


@given(precios)
def test_descuento_100_es_gratis(precio):
    assert precio_final(precio, 100) == 0


@given(precios, descuentos, descuentos)
def test_mas_descuento_no_sube_el_precio(precio, d1, d2):
    menor, mayor = sorted((d1, d2))
    assert precio_final(precio, mayor) <= precio_final(precio, menor)


# --- Entradas inválidas ---

@pytest.mark.parametrize("descuento", [-1, 100.5, 150])
def test_descuento_invalido(descuento):
    with pytest.raises(ValueError):
        precio_final(100, descuento)


def test_precio_negativo():
    with pytest.raises(ValueError):
        precio_final(-10, 10)
