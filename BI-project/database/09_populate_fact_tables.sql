-- =====================================================
-- Peuplement des tables de faits avec des données d'exemple
-- Data Warehouse - GreenCity
-- NOTE: Ces données sont optionnelles. Normalement, les tables de faits
-- sont remplies par les processus ETL (Pentaho transformations)
-- =====================================================

USE greencity_dw;

-- =====================================================
-- DATA MART 1: CONSOMMATION ÉNERGÉTIQUE
-- =====================================================

-- Fact_Consommation
-- Note: Vous devez d'abord avoir peuplé toutes les dimensions
-- et Dim_Temps doit avoir des enregistrements pour les dates utilisées

INSERT INTO Fact_Consommation (
    id_region_sk, 
    id_batiment_sk, 
    id_client_sk, 
    id_compteur_sk, 
    id_temps_sk, 
    type_energie, 
    consommation_kWh, 
    consommation_m3, 
    temperature_moyenne
)
SELECT 
    r.id_region_sk,
    b.id_batiment_sk,
    c.id_client_sk,
    compt.id_compteur_sk,
    t.id_temps_sk,
    compt.type_energie,
    CASE WHEN compt.type_energie = 'electricite' THEN 150.50 ELSE NULL END,
    CASE WHEN compt.type_energie IN ('eau', 'gaz') THEN 25.75 ELSE NULL END,
    18.5
FROM Dim_Region_Consommation r
CROSS JOIN Dim_Batiment_Consommation b ON r.id_region = b.id_region
CROSS JOIN Dim_Client_Consommation c
CROSS JOIN Dim_Compteur compt ON compt.id_batiment = b.id_batiment AND compt.id_client = c.id_client
CROSS JOIN Dim_Temps t ON t.date_complete = '2025-01-01' AND t.heure = 10
WHERE r.id_region = 'REG01'
LIMIT 10;

-- =====================================================
-- DATA MART 2: RENTABILITÉ ÉCONOMIQUE
-- =====================================================

-- Fact_Rentabilite
INSERT INTO Fact_Rentabilite (
    id_region_sk,
    id_batiment_sk,
    id_client_sk,
    id_type_energie_sk,
    id_temps_sk,
    montant_facture,
    montant_paiement,
    cout_energie,
    marge_beneficiaire,
    taux_recouvrement
)
SELECT 
    r.id_region_sk,
    b.id_batiment_sk,
    c.id_client_sk,
    te.id_type_energie_sk,
    t.id_temps_sk,
    1250.00,
    1250.00,
    950.00,
    300.00,
    100.00
FROM Dim_Region_Rentabilite r
CROSS JOIN Dim_Batiment_Rentabilite b ON r.id_region = b.id_region
CROSS JOIN Dim_Client_Rentabilite c
CROSS JOIN Dim_Type_Energie te
CROSS JOIN Dim_Temps t ON t.date_complete = '2025-01-15'
WHERE r.id_region = 'REG01'
LIMIT 10;

-- =====================================================
-- DATA MART 3: IMPACT ENVIRONNEMENTAL
-- =====================================================

-- Fact_Impact_Environnemental
INSERT INTO Fact_Impact_Environnemental (
    id_region_sk,
    id_batiment_sk,
    id_temps_sk,
    emissions_co2,
    taux_recyclage,
    consommation_totale_kWh
)
SELECT 
    r.id_region_sk,
    b.id_batiment_sk,
    t.id_temps_sk,
    125.50,
    65.75,
    850.25
FROM Dim_Region_Environnement r
CROSS JOIN Dim_Batiment_Environnement b ON r.id_region = b.id_region
CROSS JOIN Dim_Temps t ON t.date_complete = '2025-01-01'
WHERE r.id_region = 'REG01'
LIMIT 10;

-- =====================================================
-- Vérifications
-- =====================================================

SELECT 'Fact_Consommation' AS Table_Name, COUNT(*) AS Count FROM Fact_Consommation
UNION ALL
SELECT 'Fact_Rentabilite', COUNT(*) FROM Fact_Rentabilite
UNION ALL
SELECT 'Fact_Impact_Environnemental', COUNT(*) FROM Fact_Impact_Environnemental;

SELECT 'Tables de faits peuplées avec des données d''exemple' AS Resultat;
SELECT 'Note: Pour des données complètes, exécutez les transformations ETL Pentaho' AS Note;




