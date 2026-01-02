-- =====================================================
-- Data Warehouse - GreenCity
-- Trois Data Marts en architecture étoile
-- SANS colonne est_actif
-- =====================================================

CREATE DATABASE IF NOT EXISTS greencity_dw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE greencity_dw;

-- =====================================================
-- DATA MART 1: CONSOMMATION ÉNERGÉTIQUE
-- =====================================================

-- Dimension: Dim_Region
CREATE TABLE IF NOT EXISTS Dim_Region_Consommation (
    id_region_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    pays VARCHAR(50) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_region (id_region, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Batiment
CREATE TABLE IF NOT EXISTS Dim_Batiment_Consommation (
    id_batiment_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    nom_batiment VARCHAR(100) NOT NULL,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    adresse VARCHAR(200),
    superficie_m2 DECIMAL(10,2),
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_batiment (id_batiment, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Client
CREATE TABLE IF NOT EXISTS Dim_Client_Consommation (
    id_client_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_client VARCHAR(10) NOT NULL,
    nom_client VARCHAR(100) NOT NULL,
    prenom_client VARCHAR(100),
    type_client ENUM('Particulier', 'Entreprise', 'Administration'),
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_client (id_client, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Compteur
CREATE TABLE IF NOT EXISTS Dim_Compteur (
    id_compteur_sk INT AUTO_INCREMENT PRIMARY KEY,
    compteur_id VARCHAR(20) NOT NULL,
    id_batiment VARCHAR(10) NOT NULL,
    id_client VARCHAR(10) NOT NULL,
    type_energie ENUM('electricite', 'eau', 'gaz') NOT NULL,
    etat ENUM('Actif', 'Inactif', 'En maintenance'),
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_compteur (compteur_id, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Temps
CREATE TABLE IF NOT EXISTS Dim_Temps (
    id_temps_sk INT AUTO_INCREMENT PRIMARY KEY,
    date_complete DATE NOT NULL,
    annee INT NOT NULL,
    trimestre INT NOT NULL,
    mois INT NOT NULL,
    semaine INT NOT NULL,
    jour INT NOT NULL,
    jour_semaine VARCHAR(20) NOT NULL,
    est_weekend BOOLEAN NOT NULL,
    est_ferie BOOLEAN DEFAULT FALSE,
    heure INT,
    UNIQUE KEY uk_date (date_complete, heure)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table de faits: Fact_Consommation
CREATE TABLE IF NOT EXISTS Fact_Consommation (
    id_consommation BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_region_sk INT NOT NULL,
    id_batiment_sk INT NOT NULL,
    id_client_sk INT NOT NULL,
    id_compteur_sk INT NOT NULL,
    id_temps_sk INT NOT NULL,
    type_energie ENUM('electricite', 'eau', 'gaz') NOT NULL,
    consommation_kWh DECIMAL(12,2),
    consommation_m3 DECIMAL(12,2),
    temperature_moyenne DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_region_sk) REFERENCES Dim_Region_Consommation(id_region_sk),
    FOREIGN KEY (id_batiment_sk) REFERENCES Dim_Batiment_Consommation(id_batiment_sk),
    FOREIGN KEY (id_client_sk) REFERENCES Dim_Client_Consommation(id_client_sk),
    FOREIGN KEY (id_compteur_sk) REFERENCES Dim_Compteur(id_compteur_sk),
    FOREIGN KEY (id_temps_sk) REFERENCES Dim_Temps(id_temps_sk),
    INDEX idx_region (id_region_sk),
    INDEX idx_batiment (id_batiment_sk),
    INDEX idx_client (id_client_sk),
    INDEX idx_compteur (id_compteur_sk),
    INDEX idx_temps (id_temps_sk),
    INDEX idx_type_energie (type_energie)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DATA MART 2: RENTABILITÉ ÉCONOMIQUE
-- =====================================================

-- Dimension: Dim_Region_Rentabilite
CREATE TABLE IF NOT EXISTS Dim_Region_Rentabilite (
    id_region_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    pays VARCHAR(50) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_region (id_region, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Batiment_Rentabilite
CREATE TABLE IF NOT EXISTS Dim_Batiment_Rentabilite (
    id_batiment_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    nom_batiment VARCHAR(100) NOT NULL,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_batiment (id_batiment, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Client_Rentabilite
CREATE TABLE IF NOT EXISTS Dim_Client_Rentabilite (
    id_client_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_client VARCHAR(10) NOT NULL,
    nom_client VARCHAR(100) NOT NULL,
    prenom_client VARCHAR(100),
    type_client ENUM('Particulier', 'Entreprise', 'Administration'),
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_client (id_client, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Type_Energie
CREATE TABLE IF NOT EXISTS Dim_Type_Energie (
    id_type_energie_sk INT AUTO_INCREMENT PRIMARY KEY,
    type_energie ENUM('electricite', 'eau', 'gaz') NOT NULL,
    libelle VARCHAR(50) NOT NULL,
    unite_mesure VARCHAR(10) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_type_energie (type_energie, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table de faits: Fact_Rentabilite
CREATE TABLE IF NOT EXISTS Fact_Rentabilite (
    id_rentabilite BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_region_sk INT NOT NULL,
    id_batiment_sk INT NOT NULL,
    id_client_sk INT NOT NULL,
    id_type_energie_sk INT NOT NULL,
    id_temps_sk INT NOT NULL,
    montant_facture DECIMAL(10,2) NOT NULL,
    montant_paiement DECIMAL(10,2),
    cout_energie DECIMAL(10,2),
    marge_beneficiaire DECIMAL(10,2),
    taux_recouvrement DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_region_sk) REFERENCES Dim_Region_Rentabilite(id_region_sk),
    FOREIGN KEY (id_batiment_sk) REFERENCES Dim_Batiment_Rentabilite(id_batiment_sk),
    FOREIGN KEY (id_client_sk) REFERENCES Dim_Client_Rentabilite(id_client_sk),
    FOREIGN KEY (id_type_energie_sk) REFERENCES Dim_Type_Energie(id_type_energie_sk),
    FOREIGN KEY (id_temps_sk) REFERENCES Dim_Temps(id_temps_sk),
    INDEX idx_region (id_region_sk),
    INDEX idx_batiment (id_batiment_sk),
    INDEX idx_client (id_client_sk),
    INDEX idx_temps (id_temps_sk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DATA MART 3: IMPACT ENVIRONNEMENTAL
-- =====================================================

-- Dimension: Dim_Region_Environnement
CREATE TABLE IF NOT EXISTS Dim_Region_Environnement (
    id_region_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    pays VARCHAR(50) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_region (id_region, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dimension: Dim_Batiment_Environnement
CREATE TABLE IF NOT EXISTS Dim_Batiment_Environnement (
    id_batiment_sk INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    nom_batiment VARCHAR(100) NOT NULL,
    id_region VARCHAR(10) NOT NULL,
    nom_region VARCHAR(100) NOT NULL,
    date_debut_validite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_batiment (id_batiment, date_debut_validite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table de faits: Fact_Impact_Environnemental
CREATE TABLE IF NOT EXISTS Fact_Impact_Environnemental (
    id_impact BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_region_sk INT NOT NULL,
    id_batiment_sk INT NOT NULL,
    id_temps_sk INT NOT NULL,
    emissions_co2 DECIMAL(12,2),
    taux_recyclage DECIMAL(5,2),
    consommation_totale_kWh DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_region_sk) REFERENCES Dim_Region_Environnement(id_region_sk),
    FOREIGN KEY (id_batiment_sk) REFERENCES Dim_Batiment_Environnement(id_batiment_sk),
    FOREIGN KEY (id_temps_sk) REFERENCES Dim_Temps(id_temps_sk),
    INDEX idx_region (id_region_sk),
    INDEX idx_batiment (id_batiment_sk),
    INDEX idx_temps (id_temps_sk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT 'Data Warehouse créé avec succès' AS Resultat;

