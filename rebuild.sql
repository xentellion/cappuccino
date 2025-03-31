DROP TABLE coffee;
CREATE TABLE coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sort_name TEXT UNIQUE NOT NULL,
    roasting INTEGER NOT NULL,
    milled INTEGER NOT NULL,
    taste_desc TEXT NOT NULL,
    price INTEGER NOT NULL,
    volume REAL NOT NULL
);

INSERT INTO coffee 
(sort_name, roasting, milled, taste_desc, price, volume)
VALUES 
('Арабика', 3, 0, 'Описание1', 50, 0.4),
('Робуста', 3, 0, 'Описание2', 150, 0.1),
('Либерика', 3, 0, 'Описание3', 250, 0.7),
('Эксцельса', 3, 0, 'Описание4', 350, 0.3);