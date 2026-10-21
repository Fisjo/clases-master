CREATE TABLE IF NOT EXISTS videojuegos (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    plataforma VARCHAR(50),
    anio INTEGER
);

INSERT INTO videojuegos (titulo, plataforma, anio) VALUES
    ('The Legend of Zelda: Breath of the Wild', 'Switch', 2017),
    ('Hollow Knight', 'PC', 2017),
    ('God of War', 'PS4', 2018);

SELECT * FROM videojuegos;
