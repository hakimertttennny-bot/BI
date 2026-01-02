-- =====================================================
-- Initialisation de la dimension Type_Energie
-- =====================================================

USE greencity_dw;

INSERT INTO Dim_Type_Energie (type_energie, libelle, unite_mesure) VALUES
('electricite', 'Électricité', 'kWh'),
('eau', 'Eau', 'm³'),
('gaz', 'Gaz', 'm³')
ON DUPLICATE KEY UPDATE libelle = VALUES(libelle);

SELECT * FROM Dim_Type_Energie;

