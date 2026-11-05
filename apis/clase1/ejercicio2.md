# Ejercicio 2: Introducción a las APIs

## 1. ¿Qué es una API?

Una **API** (*Application Programming Interface*) es un conjunto de reglas que permite que un programa se comunique con otro. Define qué peticiones se pueden hacer, con qué formato y qué respuesta se obtiene, sin necesidad de conocer cómo funciona el sistema por dentro.

**En aplicaciones web:** el cliente (navegador, app móvil, otro servidor) envía una **petición HTTP** a una URL (*endpoint*) con un método (`GET`, `POST`, `PUT`, `DELETE`…). El servidor la procesa y devuelve una **respuesta** con un código de estado (`200`, `404`, `500`…) y normalmente datos en **JSON**.

```text
Cliente  ── GET /users/1 ──▶  Servidor (API)  ──▶  Base de datos
Cliente  ◀── 200 + JSON ───   Servidor (API)  ◀──
```

## 2. Importancia de las APIs

Las APIs son la base del software moderno porque permiten que sistemas distintos trabajen juntos. Beneficios clave:

- **Reutilización:** no hace falta reinventar servicios ya existentes (pagos, mapas, autenticación…); se consumen.
- **Integración:** conectan aplicaciones hechas en lenguajes y plataformas diferentes (web, móvil, backend).
- **Separación de responsabilidades:** el frontend y el backend se desarrollan por separado y se comunican mediante la API.
- **Escalabilidad y rapidez de desarrollo:** cada servicio puede evolucionar y escalar de forma independiente.

## 3. Ejemplos de APIs populares

| API | Descripción | Uso común | Documentación |
|---|---|---|---|
| **GitHub REST API** | Permite consultar y gestionar repositorios, usuarios, issues y pull requests. | Integraciones de CI/CD, bots, paneles de métricas, herramientas de desarrollo. | <https://docs.github.com/en/rest> |
| **Google Maps Platform** | Mapas, geocodificación, rutas y búsqueda de lugares. | Uber, Airbnb o apps de reparto para mostrar mapas y calcular rutas. | <https://developers.google.com/maps/documentation> |
| **Stripe API** | Procesa pagos, suscripciones y facturas online. | Tiendas online y plataformas SaaS que cobran con tarjeta. | <https://docs.stripe.com/api> |
| **PokéAPI** | Datos abiertos de Pokémon (especies, habilidades, movimientos). | Pokédex, juegos y proyectos de aprendizaje. | <https://pokeapi.co/docs/v2> |

## 4. Prueba real de una API (PokéAPI)

Se ha elegido **PokéAPI** porque funciona sin clave.

- **Método y URL:** `GET https://pokeapi.co/api/v2/pokemon/pikachu`
- **Código de estado:** `200 OK`
- **Cabecera relevante:** `content-type: application/json; charset=utf-8`
- **Fragmento de la respuesta:**

```json
{
  "id": 25,
  "name": "pikachu",
  "height": 4,
  "weight": 60,
  "abilities": [
    { "ability": { "name": "static" } },
    { "ability": { "name": "lightning-rod" } }
  ]
}
```

> Nota: la petición se ha lanzado con `curl` (`curl https://pokeapi.co/api/v2/pokemon/pikachu`), que hace lo mismo que Postman: mismo método, URL y respuesta. El JSON real es mucho más largo; aquí se muestran solo algunos campos.
