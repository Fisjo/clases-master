from precios import precio_final


def test_con_descuento():
    assert precio_final(100, 20) == 80

def test_sin_descuento():
    assert precio_final(50) == 50
    assert precio_final(100) == 100
    assert precio_final(150) == 150