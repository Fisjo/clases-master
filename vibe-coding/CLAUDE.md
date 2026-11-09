# Guía de trabajo
## Antes de empezar
- Lee docs/project-info.md y PLAN.md
- Si no existen, pídemelos 
- Planifica y espera a que apruebe el plan 
- Una fase cada vez, con plan aprobado
- Si hay dudas o dos opciones, pregunta 
## Convenciones
- No complicar el proyecto ni tocar archivos no solicitados
- Sin dependencias hasta que hagan falta
- Claves en .env, que nunca va a git; .env.example sin valores 
- Lógica separada de la interfaz 
## Código
- Máximo 500 líneas por archivo
- Limpio y legible para humanos
## Pruebas
- Todo va probado: cada cambio llega con su prueba en el
mismo commit 
- Si hay un bug, primero una prueba que falle; luego el
arreglo 
- Sin errores, avisos ni pruebas en rojo 
- Nada terminado sin probarlo y enseñarme el resultado 
## Git
- Commit por fase. Nunca push
- git merge, nunca git rebase 
- Nunca push: el push lo hago yo 
- Si te corrijo dos veces, propón una línea 
## Producción
- Permiso explícito para cada acción 
## Nunca
- claves reales, borrar o publicar sin preguntar 