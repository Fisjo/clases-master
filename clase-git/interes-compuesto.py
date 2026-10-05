"""Calculadora de interés compuesto ajustada a la inflación."""


def calcular_interes_compuesto(
	capital_inicial: float,
	aportacion_periodica: float,
	rentabilidad_anual: float,
	inflacion_anual: float,
	años: int,
	periodos_por_año: int = 12,
) -> tuple[float, float, float]:
	"""Devuelve (valor nominal, valor real y tasa real anual).

	Las aportaciones se realizan al final de cada periodo y el valor real se
	expresa en el poder adquisitivo de hoy.
	"""
	if años < 0 or periodos_por_año <= 0:
		raise ValueError("Los años y los periodos deben ser valores válidos.")
	if rentabilidad_anual <= -1 or inflacion_anual <= -1:
		raise ValueError("Las tasas no pueden ser inferiores o iguales a -100 %.")

	tasa_periodica = (1 + rentabilidad_anual) ** (1 / periodos_por_año) - 1
	total_periodos = años * periodos_por_año

	valor_nominal = capital_inicial * (1 + tasa_periodica) ** total_periodos
	if tasa_periodica:
		valor_nominal += aportacion_periodica * (
			((1 + tasa_periodica) ** total_periodos - 1) / tasa_periodica
		)
	else:
		valor_nominal += aportacion_periodica * total_periodos

	valor_real = valor_nominal / (1 + inflacion_anual) ** años
	tasa_real_anual = (1 + rentabilidad_anual) / (1 + inflacion_anual) - 1
	return valor_nominal, valor_real, tasa_real_anual


def pedir_numero(mensaje: str, minimo: float | None = None) -> float:
	while True:
		try:
			valor = float(input(mensaje).replace(",", "."))
			if minimo is not None and valor < minimo:
				raise ValueError
			return valor
		except ValueError:
			limite = f" (mínimo {minimo})" if minimo is not None else ""
			print(f"Introduce un número válido{limite}.")


def main() -> None:
	print("Calculadora de interés compuesto ajustada a inflación")
	capital = pedir_numero("Capital inicial (€): ", 0)
	aportacion = pedir_numero("Aportación mensual (€): ", 0)
	rentabilidad = pedir_numero("Rentabilidad anual esperada (%): ") / 100
	inflacion = pedir_numero("Inflación anual esperada (%): ") / 100
	años = int(pedir_numero("Número de años: ", 0))

	try:
		nominal, real, tasa_real = calcular_interes_compuesto(
			capital, aportacion, rentabilidad, inflacion, años
		)
	except ValueError as error:
		print(f"Error: {error}")
		return

	aportado = capital + aportacion * años * 12
	print(f"\nTotal aportado: {aportado:,.2f} €")
	print(f"Valor futuro nominal: {nominal:,.2f} €")
	print(f"Valor futuro real (poder adquisitivo actual): {real:,.2f} €")
	print(f"Rentabilidad anual real: {tasa_real * 100:.2f} %")


if __name__ == "__main__":
	main()
