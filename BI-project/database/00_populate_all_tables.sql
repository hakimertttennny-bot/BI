-- =====================================================
-- Script principal de peuplement du Data Warehouse
-- Data Warehouse - GreenCity
-- 
-- NOTE: Ce script utilise la commande SOURCE qui fonctionne dans MySQL
-- en ligne de commande. Pour MySQL Workbench ou autres clients GUI,
-- veuillez exécuter les scripts individuellement dans l'ordre indiqué
-- dans le fichier README_POPULATE.md
-- =====================================================

USE greencity_dw;

-- =====================================================
-- ÉTAPE 1: Dimensions de base (sans dépendances)
-- =====================================================

-- 1.1 Dim_Type_Energie (nécessaire pour Fact_Rentabilite)
SOURCE 05_init_dim_type_energie.sql;

-- 1.2 Dim_Temps (nécessaire pour toutes les tables de faits)
-- ATTENTION: Ce script peut prendre plusieurs minutes à s'exécuter
SOURCE 04_populate_dim_temps.sql;

-- =====================================================
-- ÉTAPE 2: Dimensions des 3 Data Marts
-- =====================================================

-- 2.1 Toutes les dimensions (Consommation, Rentabilité, Environnement)
SOURCE 08_populate_all_dimensions.sql;

-- =====================================================
-- ÉTAPE 3: Tables de faits (optionnel - données d'exemple)
-- =====================================================

-- 3.1 Tables de faits avec données d'exemple
-- NOTE: Décommentez la ligne suivante si vous voulez insérer des données d'exemple
-- dans les tables de faits. Normalement, ces tables sont remplies par les processus ETL.
-- SOURCE 09_populate_fact_tables.sql;

-- =====================================================
-- Vérification finale
-- =====================================================

SELECT '=== RÉSUMÉ DU PEUPLEMENT ===' AS '';
SELECT '';

SELECT 'Dimensions - Data Mart Consommation:' AS '';
SELECT 
    'Dim_Region_Consommation' AS Table_Name, 
    COUNT(*) AS Nombre_Enregistrements 
FROM Dim_Region_Consommation
UNION ALL
SELECT 'Dim_Batiment_Consommation', COUNT(*) FROM Dim_Batiment_Consommation
UNION ALL
SELECT 'Dim_Client_Consommation', COUNT(*) FROM Dim_Client_Consommation
UNION ALL
SELECT 'Dim_Compteur', COUNT(*) FROM Dim_Compteur;

SELECT '' AS '';
SELECT 'Dimensions - Data Mart Rentabilité:' AS '';
SELECT 
    'Dim_Region_Rentabilite' AS Table_Name, 
    COUNT(*) AS Nombre_Enregistrements 
FROM Dim_Region_Rentabilite
UNION ALL
SELECT 'Dim_Batiment_Rentabilite', COUNT(*) FROM Dim_Batiment_Rentabilite
UNION ALL
SELECT 'Dim_Client_Rentabilite', COUNT(*) FROM Dim_Client_Rentabilite
UNION ALL
SELECT 'Dim_Type_Energie', COUNT(*) FROM Dim_Type_Energie;

SELECT '' AS '';
SELECT 'Dimensions - Data Mart Environnement:' AS '';
SELECT 
    'Dim_Region_Environnement' AS Table_Name, 
    COUNT(*) AS Nombre_Enregistrements 
FROM Dim_Region_Environnement
UNION ALL
SELECT 'Dim_Batiment_Environnement', COUNT(*) FROM Dim_Batiment_Environnement;

SELECT '' AS '';
SELECT 'Dimension commune:' AS '';
SELECT 'Dim_Temps' AS Table_Name, COUNT(*) AS Nombre_Enregistrements FROM Dim_Temps;

SELECT '' AS '';
SELECT 'Tables de faits:' AS '';
SELECT 
    'Fact_Consommation' AS Table_Name, 
    COUNT(*) AS Nombre_Enregistrements 
FROM Fact_Consommation
UNION ALL
SELECT 'Fact_Rentabilite', COUNT(*) FROM Fact_Rentabilite
UNION ALL
SELECT 'Fact_Impact_Environnemental', COUNT(*) FROM Fact_Impact_Environnemental;

SELECT '' AS '';
SELECT '✅ Peuplement du Data Warehouse terminé avec succès!' AS Resultat;
SELECT 'Note: Pour remplir les tables de faits, exécutez les transformations ETL Pentaho' AS Note;

