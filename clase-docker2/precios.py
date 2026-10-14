def precio_final(precio, descuento=0):
    if precio < 0:
        raise ValueError("El precio no puede ser negativo")
    if not 0 <= descuento <= 100:
        raise ValueError("El descuento debe estar entre 0 y 100")
    return precio * (1 - descuento / 100)
