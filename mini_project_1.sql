-------------------tworzenie tabeli---------------

CREATE TABLE typee (
    typeID INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE brand (
    brandID INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE car (
    carID INTEGER PRIMARY KEY,
    brandID INTEGER,
    nazwa TEXT NOT NULL,
    typeID INTEGER,
    FOREIGN KEY (brandID) REFERENCES brand(brandID),
    FOREIGN KEY (typeID) REFERENCES typee(typeID)
);

CREATE TABLE dealer (
    dealerID INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE dealerbrand (
    dealerbrandID INTEGER PRIMARY KEY,
    brandID INTEGER,
    dealerID INTEGER,
    FOREIGN KEY (dealerID) REFERENCES dealer(dealerID),
    FOREIGN KEY (brandID) REFERENCES brand(brandID)
);

---------dodawanie informacji do tabel-----------
INSERT INTO typee (name) VALUES
    ('miejskie'),
    ('van'),
    ('suv');

INSERT INTO brand (name) VALUES
    ('seat'),
    ('renault'),
    ('subaru'),
    ('nissan'),
    ('honda');
    
INSERT INTO car (brandID, nazwa, typeID) VALUES
    (1, 'ibiza', 1),
    (1, 'alhambra', 2),
    (2, 'clio', 1),
    (3, 'forester', 3),
    (4, 'qashqai', 3),
    (5, 'cr-v', 3);

INSERT INTO dealer (name) VALUES
    ('grupa bemo'),
    ('grupa cygan'),
    ('auto lellek group');

INSERT INTO dealerbrand (dealerID, brandID) VALUES
    (1, 1),
    (2, 2),
    (2, 3),
    (3, 4);
    
    
--SELECT * FROM typee;
--SELECT * FROM brand;
--SELECT * FROM car;
--SELECT * FROM dealer;
--SELECT * FROM dealerbrand;


----dodawanie nowej kolumny i wyrażenie warunkowe----------------
ALTER TABLE car ADD COLUMN is_suv INTEGER;

UPDATE car
SET is_suv = CASE
    WHEN typeID = (SELECT typeID FROM typee WHERE name = 'suv') THEN 1
    ELSE 0
END;
    
--SELECT * FROM car;
 
    
-----usuwanie wierszy, które nie sppełniają powyższego warunku------    
DELETE FROM car
WHERE is_suv IS 0;  
    
SELECT * FROM car;


