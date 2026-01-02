-- =====================================================
-- Peuplement complet de toutes les dimensions du Data Warehouse
-- Data Warehouse - GreenCity
-- =====================================================

USE greencity_dw;

-- =====================================================
-- DATA MART 1: CONSOMMATION ÉNERGÉTIQUE
-- =====================================================

-- 1. Dim_Region_Consommation (déjà créé dans 07_populate_dim_region_consommation.sql)
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

-- 2. Dim_Batiment_Consommation
INSERT INTO Dim_Batiment_Consommation (id_batiment, nom_batiment, id_region, nom_region, adresse, superficie_m2)
VALUES 
    -- REG01
    ('BAT001', 'Bâtiment BAT001', 'REG01', 'Île-de-France', '123 Rue de Paris, 75001 Paris', 1200.00),
    ('BAT002', 'Bâtiment BAT002', 'REG01', 'Île-de-France', '456 Avenue des Champs, 75008 Paris', 2500.00),
    ('BAT003', 'Bâtiment BAT003', 'REG01', 'Île-de-France', '789 Boulevard Haussmann, 75009 Paris', 1800.00),
    -- REG02
    ('BAT101', 'Bâtiment BAT101', 'REG02', 'Provence-Alpes-Côte d''Azur', '10 Promenade des Anglais, 06000 Nice', 1500.00),
    ('BAT102', 'Bâtiment BAT102', 'REG02', 'Provence-Alpes-Côte d''Azur', '25 Rue de la République, 13001 Marseille', 3000.00),
    ('BAT103', 'Bâtiment BAT103', 'REG02', 'Provence-Alpes-Côte d''Azur', '50 Avenue du Prado, 13006 Marseille', 2200.00),
    -- REG03
    ('BAT201', 'Bâtiment BAT201', 'REG03', 'Auvergne-Rhône-Alpes', '15 Place Bellecour, 69002 Lyon', 2800.00),
    ('BAT202', 'Bâtiment BAT202', 'REG03', 'Auvergne-Rhône-Alpes', '30 Rue de la République, 69003 Lyon', 1900.00),
    -- REG04
    ('BAT301', 'Bâtiment BAT301', 'REG04', 'Nouvelle-Aquitaine', '12 Cours de l''Intendance, 33000 Bordeaux', 2100.00),
    ('BAT302', 'Bâtiment BAT302', 'REG04', 'Nouvelle-Aquitaine', '45 Rue Sainte-Catherine, 33000 Bordeaux', 1600.00),
    ('BAT303', 'Bâtiment BAT303', 'REG04', 'Nouvelle-Aquitaine', '78 Avenue Thiers, 33100 Bordeaux', 2400.00),
    ('BAT304', 'Bâtiment BAT304', 'REG04', 'Nouvelle-Aquitaine', '90 Boulevard Georges Clemenceau, 33200 Bordeaux', 1750.00),
    -- REG05
    ('BAT401', 'Bâtiment BAT401', 'REG05', 'Occitanie', '20 Place du Capitole, 31000 Toulouse', 2300.00),
    ('BAT402', 'Bâtiment BAT402', 'REG05', 'Occitanie', '55 Rue Alsace-Lorraine, 31000 Toulouse', 1400.00)
ON DUPLICATE KEY UPDATE
    nom_batiment = VALUES(nom_batiment),
    id_region = VALUES(id_region),
    nom_region = VALUES(nom_region),
    adresse = VALUES(adresse),
    superficie_m2 = VALUES(superficie_m2),
    updated_at = CURRENT_TIMESTAMP;

-- 3. Dim_Client_Consommation (50 clients)
INSERT INTO Dim_Client_Consommation (id_client, nom_client, prenom_client, type_client)
VALUES 
    ('CLI001', 'Martin', 'Jean', 'Particulier'),
    ('CLI002', 'Dubois', 'Marie', 'Particulier'),
    ('CLI003', 'Bernard', 'Pierre', 'Entreprise'),
    ('CLI004', 'Thomas', 'Sophie', 'Particulier'),
    ('CLI005', 'Robert', 'Luc', 'Administration'),
    ('CLI006', 'Petit', 'Claire', 'Particulier'),
    ('CLI007', 'Durand', 'Marc', 'Entreprise'),
    ('CLI008', 'Leroy', 'Anne', 'Particulier'),
    ('CLI009', 'Moreau', 'Paul', 'Entreprise'),
    ('CLI010', 'Simon', 'Julie', 'Particulier'),
    ('CLI011', 'Laurent', 'François', 'Administration'),
    ('CLI012', 'Lefebvre', 'Isabelle', 'Particulier'),
    ('CLI013', 'Michel', 'David', 'Entreprise'),
    ('CLI014', 'Garcia', 'Nathalie', 'Particulier'),
    ('CLI015', 'David', 'Olivier', 'Entreprise'),
    ('CLI016', 'Bertrand', 'Céline', 'Particulier'),
    ('CLI017', 'Roux', 'Michel', 'Administration'),
    ('CLI018', 'Vincent', 'Patricia', 'Particulier'),
    ('CLI019', 'Fournier', 'Stéphane', 'Entreprise'),
    ('CLI020', 'Morel', 'Valérie', 'Particulier'),
    ('CLI021', 'Girard', 'Nicolas', 'Entreprise'),
    ('CLI022', 'André', 'Caroline', 'Particulier'),
    ('CLI023', 'Lefevre', 'Christophe', 'Administration'),
    ('CLI024', 'Mercier', 'Sandrine', 'Particulier'),
    ('CLI025', 'Dupont', 'Julien', 'Entreprise'),
    ('CLI026', 'Lambert', 'Laurence', 'Particulier'),
    ('CLI027', 'Bonnet', 'Sébastien', 'Entreprise'),
    ('CLI028', 'François', 'Véronique', 'Particulier'),
    ('CLI029', 'Martinez', 'Antoine', 'Administration'),
    ('CLI030', 'Legrand', 'Christine', 'Particulier'),
    ('CLI031', 'Garnier', 'Thierry', 'Entreprise'),
    ('CLI032', 'Faure', 'Monique', 'Particulier'),
    ('CLI033', 'Rousseau', 'Frédéric', 'Entreprise'),
    ('CLI034', 'Blanc', 'Nadine', 'Particulier'),
    ('CLI035', 'Guerin', 'Bruno', 'Administration'),
    ('CLI036', 'Muller', 'Sylvie', 'Particulier'),
    ('CLI037', 'Henry', 'Jérôme', 'Entreprise'),
    ('CLI038', 'Roussel', 'Brigitte', 'Particulier'),
    ('CLI039', 'Nicolas', 'Emmanuel', 'Entreprise'),
    ('CLI040', 'Perrot', 'Danielle', 'Particulier'),
    ('CLI041', 'Morin', 'Guillaume', 'Administration'),
    ('CLI042', 'Mathieu', 'Hélène', 'Particulier'),
    ('CLI043', 'Clement', 'Yves', 'Entreprise'),
    ('CLI044', 'Gauthier', 'Dominique', 'Particulier'),
    ('CLI045', 'Dumont', 'Xavier', 'Entreprise'),
    ('CLI046', 'Lopez', 'Françoise', 'Particulier'),
    ('CLI047', 'Fontaine', 'Gilles', 'Administration'),
    ('CLI048', 'Chevalier', 'Béatrice', 'Particulier'),
    ('CLI049', 'Robin', 'Cédric', 'Entreprise'),
    ('CLI050', 'Masson', 'Éliane', 'Particulier')
ON DUPLICATE KEY UPDATE
    nom_client = VALUES(nom_client),
    prenom_client = VALUES(prenom_client),
    type_client = VALUES(type_client),
    updated_at = CURRENT_TIMESTAMP;

-- 4. Dim_Compteur
INSERT INTO Dim_Compteur (compteur_id, id_batiment, id_client, type_energie, etat)
VALUES 
    -- Compteurs électriques
    ('ELEC_001', 'BAT001', 'CLI001', 'electricite', 'Actif'),
    ('ELEC_002', 'BAT001', 'CLI002', 'electricite', 'Actif'),
    ('ELEC_003', 'BAT002', 'CLI003', 'electricite', 'Actif'),
    ('ELEC_004', 'BAT002', 'CLI004', 'electricite', 'Actif'),
    ('ELEC_005', 'BAT003', 'CLI005', 'electricite', 'Actif'),
    ('ELEC_101', 'BAT101', 'CLI006', 'electricite', 'Actif'),
    ('ELEC_102', 'BAT101', 'CLI007', 'electricite', 'Actif'),
    ('ELEC_103', 'BAT102', 'CLI008', 'electricite', 'Actif'),
    ('ELEC_104', 'BAT102', 'CLI009', 'electricite', 'Actif'),
    ('ELEC_105', 'BAT103', 'CLI010', 'electricite', 'Actif'),
    ('ELEC_201', 'BAT201', 'CLI011', 'electricite', 'Actif'),
    ('ELEC_202', 'BAT201', 'CLI012', 'electricite', 'Actif'),
    ('ELEC_203', 'BAT202', 'CLI013', 'electricite', 'Actif'),
    ('ELEC_301', 'BAT301', 'CLI014', 'electricite', 'Actif'),
    ('ELEC_302', 'BAT301', 'CLI015', 'electricite', 'Actif'),
    ('ELEC_303', 'BAT302', 'CLI016', 'electricite', 'Actif'),
    ('ELEC_304', 'BAT303', 'CLI017', 'electricite', 'Actif'),
    ('ELEC_305', 'BAT304', 'CLI018', 'electricite', 'Actif'),
    ('ELEC_401', 'BAT401', 'CLI019', 'electricite', 'Actif'),
    ('ELEC_402', 'BAT402', 'CLI020', 'electricite', 'Actif'),
    -- Compteurs eau
    ('EAU_001', 'BAT001', 'CLI001', 'eau', 'Actif'),
    ('EAU_002', 'BAT001', 'CLI002', 'eau', 'Actif'),
    ('EAU_003', 'BAT002', 'CLI003', 'eau', 'Actif'),
    ('EAU_004', 'BAT002', 'CLI004', 'eau', 'Actif'),
    ('EAU_005', 'BAT003', 'CLI005', 'eau', 'Actif'),
    ('EAU_101', 'BAT101', 'CLI006', 'eau', 'Actif'),
    ('EAU_102', 'BAT101', 'CLI007', 'eau', 'Actif'),
    ('EAU_103', 'BAT102', 'CLI008', 'eau', 'Actif'),
    ('EAU_104', 'BAT102', 'CLI009', 'eau', 'Actif'),
    ('EAU_105', 'BAT103', 'CLI010', 'eau', 'Actif'),
    ('EAU_201', 'BAT201', 'CLI011', 'eau', 'Actif'),
    ('EAU_202', 'BAT201', 'CLI012', 'eau', 'Actif'),
    ('EAU_203', 'BAT202', 'CLI013', 'eau', 'Actif'),
    ('EAU_301', 'BAT301', 'CLI014', 'eau', 'Actif'),
    ('EAU_302', 'BAT301', 'CLI015', 'eau', 'Actif'),
    ('EAU_303', 'BAT302', 'CLI016', 'eau', 'Actif'),
    ('EAU_304', 'BAT303', 'CLI017', 'eau', 'Actif'),
    ('EAU_305', 'BAT304', 'CLI018', 'eau', 'Actif'),
    ('EAU_401', 'BAT401', 'CLI019', 'eau', 'Actif'),
    ('EAU_402', 'BAT402', 'CLI020', 'eau', 'Actif'),
    -- Compteurs gaz
    ('GAZ_001', 'BAT001', 'CLI021', 'gaz', 'Actif'),
    ('GAZ_002', 'BAT001', 'CLI022', 'gaz', 'Actif'),
    ('GAZ_003', 'BAT002', 'CLI023', 'gaz', 'Actif'),
    ('GAZ_004', 'BAT002', 'CLI024', 'gaz', 'Actif'),
    ('GAZ_005', 'BAT003', 'CLI025', 'gaz', 'Actif'),
    ('GAZ_101', 'BAT101', 'CLI026', 'gaz', 'Actif'),
    ('GAZ_102', 'BAT101', 'CLI027', 'gaz', 'Actif'),
    ('GAZ_103', 'BAT102', 'CLI028', 'gaz', 'Actif'),
    ('GAZ_104', 'BAT102', 'CLI029', 'gaz', 'Actif'),
    ('GAZ_105', 'BAT103', 'CLI030', 'gaz', 'Actif'),
    ('GAZ_201', 'BAT201', 'CLI031', 'gaz', 'Actif'),
    ('GAZ_202', 'BAT201', 'CLI032', 'gaz', 'Actif'),
    ('GAZ_203', 'BAT202', 'CLI033', 'gaz', 'Actif'),
    ('GAZ_301', 'BAT301', 'CLI034', 'gaz', 'Actif'),
    ('GAZ_302', 'BAT301', 'CLI035', 'gaz', 'Actif'),
    ('GAZ_303', 'BAT302', 'CLI036', 'gaz', 'Actif'),
    ('GAZ_304', 'BAT303', 'CLI037', 'gaz', 'Actif'),
    ('GAZ_305', 'BAT304', 'CLI038', 'gaz', 'Actif'),
    ('GAZ_401', 'BAT401', 'CLI039', 'gaz', 'Actif'),
    ('GAZ_402', 'BAT402', 'CLI040', 'gaz', 'Actif')
ON DUPLICATE KEY UPDATE
    id_batiment = VALUES(id_batiment),
    id_client = VALUES(id_client),
    type_energie = VALUES(type_energie),
    etat = VALUES(etat),
    updated_at = CURRENT_TIMESTAMP;

-- Note: Dim_Temps est rempli par le script 04_populate_dim_temps.sql

-- =====================================================
-- DATA MART 2: RENTABILITÉ ÉCONOMIQUE
-- =====================================================

-- 5. Dim_Region_Rentabilite
INSERT INTO Dim_Region_Rentabilite (id_region, nom_region, pays)
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

-- 6. Dim_Batiment_Rentabilite
INSERT INTO Dim_Batiment_Rentabilite (id_batiment, nom_batiment, id_region, nom_region)
VALUES 
    ('BAT001', 'Bâtiment BAT001', 'REG01', 'Île-de-France'),
    ('BAT002', 'Bâtiment BAT002', 'REG01', 'Île-de-France'),
    ('BAT003', 'Bâtiment BAT003', 'REG01', 'Île-de-France'),
    ('BAT101', 'Bâtiment BAT101', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT102', 'Bâtiment BAT102', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT103', 'Bâtiment BAT103', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT201', 'Bâtiment BAT201', 'REG03', 'Auvergne-Rhône-Alpes'),
    ('BAT202', 'Bâtiment BAT202', 'REG03', 'Auvergne-Rhône-Alpes'),
    ('BAT301', 'Bâtiment BAT301', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT302', 'Bâtiment BAT302', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT303', 'Bâtiment BAT303', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT304', 'Bâtiment BAT304', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT401', 'Bâtiment BAT401', 'REG05', 'Occitanie'),
    ('BAT402', 'Bâtiment BAT402', 'REG05', 'Occitanie')
ON DUPLICATE KEY UPDATE
    nom_batiment = VALUES(nom_batiment),
    id_region = VALUES(id_region),
    nom_region = VALUES(nom_region),
    updated_at = CURRENT_TIMESTAMP;

-- 7. Dim_Client_Rentabilite
INSERT INTO Dim_Client_Rentabilite (id_client, nom_client, prenom_client, type_client)
SELECT id_client, nom_client, prenom_client, type_client
FROM Dim_Client_Consommation
ON DUPLICATE KEY UPDATE
    nom_client = VALUES(nom_client),
    prenom_client = VALUES(prenom_client),
    type_client = VALUES(type_client),
    updated_at = CURRENT_TIMESTAMP;

-- Note: Dim_Type_Energie est rempli par le script 05_init_dim_type_energie.sql

-- =====================================================
-- DATA MART 3: IMPACT ENVIRONNEMENTAL
-- =====================================================

-- 8. Dim_Region_Environnement
INSERT INTO Dim_Region_Environnement (id_region, nom_region, pays)
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

-- 9. Dim_Batiment_Environnement
INSERT INTO Dim_Batiment_Environnement (id_batiment, nom_batiment, id_region, nom_region)
VALUES 
    ('BAT001', 'Bâtiment BAT001', 'REG01', 'Île-de-France'),
    ('BAT002', 'Bâtiment BAT002', 'REG01', 'Île-de-France'),
    ('BAT003', 'Bâtiment BAT003', 'REG01', 'Île-de-France'),
    ('BAT101', 'Bâtiment BAT101', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT102', 'Bâtiment BAT102', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT103', 'Bâtiment BAT103', 'REG02', 'Provence-Alpes-Côte d''Azur'),
    ('BAT201', 'Bâtiment BAT201', 'REG03', 'Auvergne-Rhône-Alpes'),
    ('BAT202', 'Bâtiment BAT202', 'REG03', 'Auvergne-Rhône-Alpes'),
    ('BAT301', 'Bâtiment BAT301', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT302', 'Bâtiment BAT302', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT303', 'Bâtiment BAT303', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT304', 'Bâtiment BAT304', 'REG04', 'Nouvelle-Aquitaine'),
    ('BAT401', 'Bâtiment BAT401', 'REG05', 'Occitanie'),
    ('BAT402', 'Bâtiment BAT402', 'REG05', 'Occitanie')
ON DUPLICATE KEY UPDATE
    nom_batiment = VALUES(nom_batiment),
    id_region = VALUES(id_region),
    nom_region = VALUES(nom_region),
    updated_at = CURRENT_TIMESTAMP;

-- =====================================================
-- Vérifications
-- =====================================================

SELECT 'Dim_Region_Consommation' AS Table_Name, COUNT(*) AS Count FROM Dim_Region_Consommation
UNION ALL
SELECT 'Dim_Batiment_Consommation', COUNT(*) FROM Dim_Batiment_Consommation
UNION ALL
SELECT 'Dim_Client_Consommation', COUNT(*) FROM Dim_Client_Consommation
UNION ALL
SELECT 'Dim_Compteur', COUNT(*) FROM Dim_Compteur
UNION ALL
SELECT 'Dim_Region_Rentabilite', COUNT(*) FROM Dim_Region_Rentabilite
UNION ALL
SELECT 'Dim_Batiment_Rentabilite', COUNT(*) FROM Dim_Batiment_Rentabilite
UNION ALL
SELECT 'Dim_Client_Rentabilite', COUNT(*) FROM Dim_Client_Rentabilite
UNION ALL
SELECT 'Dim_Type_Energie', COUNT(*) FROM Dim_Type_Energie
UNION ALL
SELECT 'Dim_Region_Environnement', COUNT(*) FROM Dim_Region_Environnement
UNION ALL
SELECT 'Dim_Batiment_Environnement', COUNT(*) FROM Dim_Batiment_Environnement;

SELECT 'Toutes les dimensions ont été peuplées avec succès' AS Resultat;

