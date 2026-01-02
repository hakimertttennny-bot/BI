-- =====================================================
-- Peuplement de la dimension Dim_Region_Consommation
-- Data Warehouse - GreenCity
-- =====================================================

USE greencity_dw;

-- Insertion des régions dans la dimension
-- Les régions correspondent à celles de la base opérationnelle

INSERT INTO Dim_Region_Consommation (id_region, nom_region, pays)
VALUES 
    ('REG01', 'Île-de-France', 'France'),
    ('REG02', 'Provence-Alpes-Côte d''Azur', 'France'),
    ('REG03', 'Auvergne-Rhône-Alpes', 'France'),
    ('REG04', 'Nouvelle-Aquitaine', 'France'),
    ('REG05', 'Occitanie', 'France')
ON DUPLICATE KEY UPDATE
    nom_region = VALUES(nom_region),
    pays = VALUES(pays),
    updated_at = CURRENT_TIMESTAMP;

-- Vérification
SELECT * FROM Dim_Region_Consommation ORDER BY id_region;




