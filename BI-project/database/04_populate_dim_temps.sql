-- =====================================================
-- Remplissage de la dimension Temps
-- Période : 2020-2030 avec toutes les heures
-- Compatible XAMPP (MySQL/MariaDB)
-- =====================================================

USE greencity_dw;

-- Supprimer les données existantes si nécessaire (décommenter si besoin)
-- TRUNCATE TABLE Dim_Temps;

-- Procédure stockée compatible XAMPP
DELIMITER $$

DROP PROCEDURE IF EXISTS PopulateDimTemps$$

CREATE PROCEDURE PopulateDimTemps()
BEGIN
    DECLARE v_date DATE DEFAULT '2020-01-01';
    DECLARE v_heure INT DEFAULT 0;
    DECLARE v_annee INT;
    DECLARE v_trimestre INT;
    DECLARE v_mois INT;
    DECLARE v_semaine INT;
    DECLARE v_jour INT;
    DECLARE v_jour_semaine VARCHAR(20);
    DECLARE v_est_weekend BOOLEAN;
    
    -- Boucle sur les dates de 2020 à 2030
    date_loop: WHILE v_date <= '2030-12-31' DO
        -- Calculer les valeurs une seule fois par date (optimisation)
        SET v_annee = YEAR(v_date);
        SET v_trimestre = QUARTER(v_date);
        SET v_mois = MONTH(v_date);
        SET v_semaine = WEEK(v_date, 1);
        SET v_jour = DAY(v_date);
        SET v_jour_semaine = DAYNAME(v_date);
        SET v_est_weekend = (DAYOFWEEK(v_date) IN (1, 7));
        
        SET v_heure = 0;
        
        -- Boucle sur les heures (0-23)
        heure_loop: WHILE v_heure < 24 DO
            INSERT INTO Dim_Temps (
                date_complete, 
                annee, 
                trimestre, 
                mois, 
                semaine, 
                jour, 
                jour_semaine, 
                est_weekend, 
                est_ferie, 
                heure
            ) VALUES (
                v_date,
                v_annee,
                v_trimestre,
                v_mois,
                v_semaine,
                v_jour,
                v_jour_semaine,
                v_est_weekend,
                0,
                v_heure
            )
            ON DUPLICATE KEY UPDATE 
                annee = v_annee,
                trimestre = v_trimestre,
                mois = v_mois,
                semaine = v_semaine,
                jour = v_jour,
                jour_semaine = v_jour_semaine,
                est_weekend = v_est_weekend,
                est_ferie = 0;
            
            SET v_heure = v_heure + 1;
        END WHILE heure_loop;
        
        SET v_date = DATE_ADD(v_date, INTERVAL 1 DAY);
    END WHILE date_loop;
END$$

DELIMITER ;

-- Exécuter la procédure
CALL PopulateDimTemps();

-- Supprimer la procédure après utilisation
DROP PROCEDURE IF EXISTS PopulateDimTemps;

-- Vérification
SELECT 
    COUNT(*) AS total_lignes,
    MIN(date_complete) AS date_min,
    MAX(date_complete) AS date_max,
    MIN(heure) AS heure_min,
    MAX(heure) AS heure_max
FROM Dim_Temps;

SELECT 'Dimension Temps remplie avec succès' AS Resultat;
