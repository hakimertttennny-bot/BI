-- =====================================================
-- Suppression de la colonne est_actif des tables de dimensions
-- MySQL ne supporte pas DROP COLUMN IF EXISTS
-- Utiliser cette procédure stockée pour supprimer si elle existe
-- =====================================================

USE greencity_dw;

DELIMITER $$

-- Procédure pour supprimer une colonne si elle existe
DROP PROCEDURE IF EXISTS DropColumnIfExists$$

CREATE PROCEDURE DropColumnIfExists(
    IN tableName VARCHAR(64),
    IN columnName VARCHAR(64)
)
BEGIN
    DECLARE columnExists INT DEFAULT 0;
    
    SELECT COUNT(*) INTO columnExists
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = tableName
      AND COLUMN_NAME = columnName;
    
    IF columnExists > 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', tableName, ' DROP COLUMN ', columnName);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END$$

DELIMITER ;

-- DATA MART 1: CONSOMMATION ÉNERGÉTIQUE
CALL DropColumnIfExists('Dim_Region_Consommation', 'est_actif');
CALL DropColumnIfExists('Dim_Batiment_Consommation', 'est_actif');
CALL DropColumnIfExists('Dim_Client_Consommation', 'est_actif');
CALL DropColumnIfExists('Dim_Compteur', 'est_actif');

-- DATA MART 2: RENTABILITÉ ÉCONOMIQUE
CALL DropColumnIfExists('Dim_Region_Rentabilite', 'est_actif');
CALL DropColumnIfExists('Dim_Batiment_Rentabilite', 'est_actif');
CALL DropColumnIfExists('Dim_Client_Rentabilite', 'est_actif');
CALL DropColumnIfExists('Dim_Type_Energie', 'est_actif');

-- DATA MART 3: IMPACT ENVIRONNEMENTAL
CALL DropColumnIfExists('Dim_Region_Environnement', 'est_actif');
CALL DropColumnIfExists('Dim_Batiment_Environnement', 'est_actif');

-- Supprimer la procédure après utilisation
DROP PROCEDURE IF EXISTS DropColumnIfExists;

-- Note: Dim_Temps n'a pas de colonne est_actif dans le script original

SELECT 'Colonnes est_actif supprimées avec succès' AS Resultat;

