-- =====================================================
-- Base de Données Opérationnelle - GreenCity
-- =====================================================

CREATE DATABASE IF NOT EXISTS greencity_operational CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE greencity_operational;

-- =====================================================
-- Table: regions
-- =====================================================
CREATE TABLE IF NOT EXISTS regions (
    id_region VARCHAR(10) PRIMARY KEY,
    nom_region VARCHAR(100) NOT NULL,
    pays VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: batiments
-- =====================================================
CREATE TABLE IF NOT EXISTS batiments (
    id_batiment VARCHAR(10) PRIMARY KEY,
    id_region VARCHAR(10) NOT NULL,
    nom_batiment VARCHAR(100) NOT NULL,
    adresse VARCHAR(200),
    superficie_m2 DECIMAL(10,2),
    date_construction DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_region) REFERENCES regions(id_region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: clients
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
    id_client VARCHAR(10) PRIMARY KEY,
    nom_client VARCHAR(100) NOT NULL,
    prenom_client VARCHAR(100),
    type_client ENUM('Particulier', 'Entreprise', 'Administration') NOT NULL,
    email VARCHAR(100),
    telephone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: compteurs
-- =====================================================
CREATE TABLE IF NOT EXISTS compteurs (
    compteur_id VARCHAR(20) PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    id_client VARCHAR(10) NOT NULL,
    type_energie ENUM('electricite', 'eau', 'gaz') NOT NULL,
    etat ENUM('Actif', 'Inactif', 'En maintenance') DEFAULT 'Actif',
    date_installation DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_batiment) REFERENCES batiments(id_batiment),
    FOREIGN KEY (id_client) REFERENCES clients(id_client)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: factures
-- =====================================================
CREATE TABLE IF NOT EXISTS factures (
    id_facture INT AUTO_INCREMENT PRIMARY KEY,
    id_client VARCHAR(10) NOT NULL,
    compteur_id VARCHAR(20) NOT NULL,
    date_facture DATE NOT NULL,
    montant_total DECIMAL(10,2) NOT NULL,
    consommation_kWh DECIMAL(12,2),
    consommation_m3 DECIMAL(12,2),
    etat_paiement ENUM('Payée', 'En attente', 'Impayée') DEFAULT 'En attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_client) REFERENCES clients(id_client),
    FOREIGN KEY (compteur_id) REFERENCES compteurs(compteur_id),
    INDEX idx_date_facture (date_facture),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: paiements
-- =====================================================
CREATE TABLE IF NOT EXISTS paiements (
    id_paiement INT AUTO_INCREMENT PRIMARY KEY,
    id_facture INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    date_paiement DATE NOT NULL,
    methode_paiement ENUM('Carte bancaire', 'Virement', 'Chèque', 'Espèces') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_facture) REFERENCES factures(id_facture),
    INDEX idx_date_paiement (date_paiement),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: couts_energie
-- =====================================================
CREATE TABLE IF NOT EXISTS couts_energie (
    id_cout INT AUTO_INCREMENT PRIMARY KEY,
    type_energie ENUM('electricite', 'eau', 'gaz') NOT NULL,
    prix_unitaire DECIMAL(10,4) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type_energie (type_energie),
    INDEX idx_dates (date_debut, date_fin)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Table: temperatures
-- =====================================================
CREATE TABLE IF NOT EXISTS temperatures (
    id_temperature INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment VARCHAR(10) NOT NULL,
    date_mesure DATETIME NOT NULL,
    temperature_celsius DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_batiment) REFERENCES batiments(id_batiment),
    INDEX idx_date_mesure (date_mesure),
    INDEX idx_batiment (id_batiment)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- Index supplémentaires pour optimiser les requêtes
-- =====================================================
CREATE INDEX idx_batiments_region ON batiments(id_region);
CREATE INDEX idx_compteurs_batiment ON compteurs(id_batiment);
CREATE INDEX idx_compteurs_client ON compteurs(id_client);
CREATE INDEX idx_factures_client ON factures(id_client);
CREATE INDEX idx_factures_compteur ON factures(compteur_id);

SELECT 'Base de données opérationnelle créée avec succès' AS Resultat;

