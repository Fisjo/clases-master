-- Práctica

CREATE TABLE departamentos(
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre                  VARCHAR(100) NOT NULL
);

CREATE TABLE empleados(
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre                  VARCHAR(100) NOT NULL,
    email                   VARCHAR(100) NOT NULL,
    salario                 NUMERIC(8,2) NOT NULL,
    departamento_id         BIGINT REFERENCES departamentos(id)
);

CREATE TABLE proyectos(
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre                  VARCHAR(100) NOT NULL,
    fecha_inicio            TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    departamento_id         BIGINT REFERENCES departamentos(id)
);

INSERT INTO departamentos (nombre) VALUES
('Ventas'), ('Tecnología'), ('Legal'), ('I+D');

INSERT INTO empleados
(nombre, email, salario, departamento_id)
VALUES
('Ana', 'ana@empresa.com', 52000, 2),
('Luis', 'luis@empresa.com', 38000, 2),
('Marta', 'marta@empresa.com', 45000, 1),
('Pablo', 'pablo@empresa.com', 31000, 1),
('Sara', 'sara@empresa.com', 29000, NULL);
-- Empleados (Sara no tiene departamento)

INSERT INTO proyectos
(nombre, fecha_inicio, departamento_id)
VALUES
('Web nueva', '2026-09-01', 2),
('App móvil', '2026-11-15', 2),
('Campaña de verano', '2027-05-01', 1);
-- Legal e I+D no tienen empleados ni proyectos


SELECT departamentos.nombre AS departamento
FROM departamentos
INNER JOIN empleados ON departamentos.id = empleados.departamento_id
WHERE empleados.nombre = 'Sara';

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM departamentos
INNER JOIN empleados ON departamentos.id = empleados.departamento_id;

-- EXTRA: Comparacion de joins

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM departamentos
LEFT JOIN empleados ON departamentos.id = empleados.departamento_id;
--NULL en I+D y Legal

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM departamentos
RIGHT JOIN empleados ON departamentos.id = empleados.departamento_id;
-- Sarah = NULL

SELECT empleados.nombre AS empleado, departamentos.nombre AS departamento
FROM departamentos
FULL OUTER JOIN empleados ON departamentos.id = empleados.departamento_id;
-- NULL en I+D y Legal + Sarah = NULL


-- Práctica 2

SELECT empleados.nombre AS empleados, empleados.salario AS salario
FROM empleados
WHERE empleados.salario < (
    SELECT AVG(empleados.salario)
    FROM empleados
);
    
SELECT empleados.nombre AS empleados, empleados.salario AS salario
FROM empleados
WHERE empleados.salario = (
    SELECT MAX(empleados.salario)
    FROM empleados
);

SELECT empleados.nombre AS empleados, departamentos.nombre AS departamento
FROM empleados
INNER JOIN departamentos ON empleados.departamento_id = departamentos.id
WHERE empleados.departamento_id = (
    SELECT departamentos.id
    FROM departamentos
    WHERE departamentos.nombre = 'Tecnología'
);
