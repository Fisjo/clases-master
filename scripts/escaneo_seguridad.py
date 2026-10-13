"""Simula un escaneo de seguridad buscando claves API expuestas en un archivo."""
import re
import sys

PATRONES = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}"),
]


def main(ruta):
    with open(ruta, encoding="utf-8") as f:
        lineas = f.readlines()

    hallazgos = [
        (n, linea.strip())
        for n, linea in enumerate(lineas, start=1)
        for patron in PATRONES
        if patron.search(linea)
    ]

    if hallazgos:
        print(f"Posibles claves expuestas en {ruta}:")
        for n, linea in hallazgos:
            print(f"  línea {n}: {linea}")
        return 1

    print(f"Sin claves API expuestas en {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "ventas.json"))
