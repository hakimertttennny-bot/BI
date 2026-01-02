"""
Script de génération de données pour GreenCity
Génère des fichiers CSV et JSON avec des défauts de qualité intentionnels
"""

import json
import csv
import random
import os
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

# Obtenir le répertoire du projet (parent du répertoire scripts)
PROJECT_ROOT = Path(__file__).parent.parent

fake = Faker('fr_FR')

# Configuration
REGIONS = ["REG01", "REG02", "REG03", "REG04", "REG05"]
BATIMENTS = {
    "REG01": ["BAT001", "BAT002", "BAT003"],
    "REG02": ["BAT101", "BAT102", "BAT103"],
    "REG03": ["BAT201", "BAT202"],
    "REG04": ["BAT301", "BAT302", "BAT303", "BAT304"],
    "REG05": ["BAT401", "BAT402"]
}

COMPTEURS_ELEC = ["ELEC_001", "ELEC_002", "ELEC_101", "ELEC_102", "ELEC_201", "ELEC_202"]
COMPTEURS_EAU = ["EAU_001", "EAU_002", "EAU_101", "EAU_102", "EAU_201", "EAU_202"]
COMPTEURS_GAZ = ["GAZ_001", "GAZ_002", "GAZ_101", "GAZ_102", "GAZ_201", "GAZ_202"]

def generate_json_consumption(type_energie, mois, annee):
    """Génère un fichier JSON de consommation"""
    date_gen = f"{annee}-{mois:02d}-14"
    
    data = {
        "id_region": random.choice(REGIONS),
        "batiments": []
    }
    
    for id_region, batiments_list in BATIMENTS.items():
        for id_batiment in batiments_list:
            if random.random() > 0.1:  # 90% de chance d'inclure le bâtiment
                batiment_data = {
                    "id_batiment": id_batiment,
                    "type_energie": type_energie,
                    "unite": "KWh" if type_energie == "electricite" else "m3",
                    "date_generation": date_gen,
                    "mesures": []
                }
                
                # Générer des mesures horaires pour le mois
                jours = 28 if mois == 2 else 30 if mois in [4, 6, 9, 11] else 31
                compteurs = COMPTEURS_ELEC if type_energie == "electricite" else (COMPTEURS_EAU if type_energie == "eau" else COMPTEURS_GAZ)
                
                for jour in range(1, jours + 1):
                    for heure in range(8, 20):  # De 8h à 19h
                        if random.random() > 0.05:  # 95% de chance d'avoir une mesure
                            compteur_id = random.choice(compteurs)
                            date_mesure = f"{annee}-{mois:02d}-{jour:02d}T{heure:02d}:00:00"
                            
                            if type_energie == "electricite":
                                consommation = round(random.uniform(50, 200), 1)
                                mesure = {
                                    "compteur_id": compteur_id,
                                    "date_mesure": date_mesure,
                                    "consommation_kWh": consommation
                                }
                            elif type_energie == "eau":
                                consommation = round(random.uniform(0.5, 5.0), 2)
                                mesure = {
                                    "compteur_id": compteur_id,
                                    "date_mesure": date_mesure,
                                    "consommation_m3": consommation
                                }
                            else:  # gaz
                                consommation = round(random.uniform(1.0, 10.0), 2)
                                mesure = {
                                    "compteur_id": compteur_id,
                                    "date_mesure": date_mesure,
                                    "consommation_m3": consommation
                                }
                            
                            # Introduire des défauts de qualité
                            if random.random() < 0.05:  # 5% de valeurs manquantes
                                if type_energie == "electricite":
                                    mesure["consommation_kWh"] = None
                                else:
                                    mesure["consommation_m3"] = None
                            
                            if random.random() < 0.03:  # 3% de dates incorrectes
                                mesure["date_mesure"] = "invalid-date"
                            
                            batiment_data["mesures"].append(mesure)
                
                if batiment_data["mesures"]:
                    data["batiments"].append(batiment_data)
    
    # Sauvegarder le fichier JSON
    filename = PROJECT_ROOT / f"data/source/{type_energie.capitalize()}_consumption_{mois:02d}_{annee}.json"
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Fichier généré: {filename}")
    return str(filename)

def generate_csv_environmental(mois, annee):
    """Génère un fichier CSV de rapports environnementaux"""
    filename = PROJECT_ROOT / f"data/source/env_reports_{mois:02d}_{annee}.csv"
    filename.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id_region', 'id_batiment', 'date_rapport', 'emission_CO2_kg', 'taux_recyclage'])
        
        for id_region, batiments_list in BATIMENTS.items():
            for id_batiment in batiments_list:
                if random.random() > 0.1:  # 90% de chance d'inclure
                    date_rapport = f"{annee}-{mois:02d}-28"
                    emission_CO2 = random.randint(200, 800)
                    taux_recyclage = round(random.uniform(0.50, 0.95), 2)
                    
                    # Introduire des défauts de qualité
                    if random.random() < 0.05:  # 5% de valeurs manquantes
                        emission_CO2 = ""
                    
                    if random.random() < 0.03:  # 3% de dates incorrectes
                        date_rapport = "invalid-date"
                    
                    if random.random() < 0.02:  # 2% d'espaces inutiles
                        id_batiment = f" {id_batiment} "
                    
                    writer.writerow([id_region, id_batiment, date_rapport, emission_CO2, taux_recyclage])
    
    print(f"Fichier généré: {filename}")
    return str(filename)

def generate_sql_insert_data():
    """Génère un script SQL avec des données d'exemple"""
    sql_content = []
    sql_content.append("-- Données d'exemple pour la base opérationnelle\n")
    sql_content.append("USE greencity_operational;\n\n")
    
    # Régions
    sql_content.append("-- Insertion des régions\n")
    regions_data = [
        ("REG01", "Île-de-France", "France"),
        ("REG02", "Provence-Alpes-Côte d'Azur", "France"),
        ("REG03", "Auvergne-Rhône-Alpes", "France"),
        ("REG04", "Nouvelle-Aquitaine", "France"),
        ("REG05", "Occitanie", "France")
    ]
    for id_reg, nom, pays in regions_data:
        sql_content.append(f"INSERT INTO regions (id_region, nom_region, pays) VALUES ('{id_reg}', '{nom}', '{pays}');\n")
    
    # Bâtiments
    sql_content.append("\n-- Insertion des bâtiments\n")
    for id_region, batiments_list in BATIMENTS.items():
        for id_batiment in batiments_list:
            nom = f"Bâtiment {id_batiment}"
            adresse = fake.address().replace("'", "''")
            superficie = random.randint(500, 5000)
            date_const = fake.date_between(start_date='-10y', end_date='today')
            sql_content.append(f"INSERT INTO batiments (id_batiment, id_region, nom_batiment, adresse, superficie_m2, date_construction) VALUES ('{id_batiment}', '{id_region}', '{nom}', '{adresse}', {superficie}, '{date_const}');\n")
    
    # Clients
    sql_content.append("\n-- Insertion des clients\n")
    for i in range(1, 51):
        id_client = f"CLI{i:03d}"
        nom = fake.last_name().replace("'", "''")
        prenom = fake.first_name().replace("'", "''")
        email = fake.email()
        tel = fake.phone_number()
        type_client = random.choice(['Particulier', 'Entreprise', 'Administration'])
        sql_content.append(f"INSERT INTO clients (id_client, nom_client, prenom_client, email, telephone, type_client) VALUES ('{id_client}', '{nom}', '{prenom}', '{email}', '{tel}', '{type_client}');\n")
    
    # Compteurs
    sql_content.append("\n-- Insertion des compteurs\n")
    client_ids = [f"CLI{i:03d}" for i in range(1, 51)]
    for id_region, batiments_list in BATIMENTS.items():
        for id_batiment in batiments_list:
            for compteur_id in COMPTEURS_ELEC[:2]:
                id_client = random.choice(client_ids)
                date_inst = fake.date_between(start_date='-5y', end_date='today')
                sql_content.append(f"INSERT INTO compteurs (compteur_id, id_batiment, id_client, type_energie, date_installation, etat) VALUES ('{compteur_id}', '{id_batiment}', '{id_client}', 'electricite', '{date_inst}', 'Actif');\n")
    
    # Factures et paiements (exemples)
    sql_content.append("\n-- Insertion de factures et paiements (exemples)\n")
    for i in range(1, 101):
        id_facture = f"FAC{i:05d}"
        id_client = random.choice(client_ids)
        id_batiment = random.choice([b for bat_list in BATIMENTS.values() for b in bat_list])
        compteur_id = random.choice(COMPTEURS_ELEC)
        date_fact = fake.date_between(start_date='-1y', end_date='today')
        date_debut = date_fact - timedelta(days=30)
        date_fin = date_fact
        consommation = random.randint(100, 2000)
        prix_unit = round(random.uniform(0.10, 0.25), 4)
        montant_HT = round(consommation * prix_unit, 2)
        montant_TTC = round(montant_HT * 1.20, 2)
        statut = random.choice(['Emise', 'Payée', 'Impayée'])
        
        sql_content.append(f"INSERT INTO factures (id_facture, id_client, id_batiment, compteur_id, date_facturation, date_debut_periode, date_fin_periode, consommation_kWh, prix_unitaire, montant_HT, montant_TTC, statut) VALUES ('{id_facture}', '{id_client}', '{id_batiment}', '{compteur_id}', '{date_fact}', '{date_debut}', '{date_fin}', {consommation}, {prix_unit}, {montant_HT}, {montant_TTC}, '{statut}');\n")
        
        if statut == 'Payée':
            id_paiement = f"PAY{i:05d}"
            date_paiement = date_fact + timedelta(days=random.randint(1, 30))
            mode = random.choice(['Carte bancaire', 'Virement', 'Chèque'])
            sql_content.append(f"INSERT INTO paiements (id_paiement, id_facture, id_client, montant_paye, date_paiement, mode_paiement, statut) VALUES ('{id_paiement}', '{id_facture}', '{id_client}', {montant_TTC}, '{date_paiement}', '{mode}', 'Validé');\n")
    
    # Écrire le fichier SQL
    sql_file = PROJECT_ROOT / 'database/03_insert_sample_data.sql'
    sql_file.parent.mkdir(parents=True, exist_ok=True)
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.writelines(sql_content)
    
    print(f"Fichier SQL généré: {sql_file}")

if __name__ == "__main__":
    # Créer les répertoires nécessaires
    (PROJECT_ROOT / "data/source").mkdir(parents=True, exist_ok=True)
    
    # Générer des données pour plusieurs mois
    for mois in range(1, 13):
        generate_json_consumption("electricite", mois, 2025)
        generate_json_consumption("eau", mois, 2025)
        generate_json_consumption("gaz", mois, 2025)
        generate_csv_environmental(mois, 2025)
    
    generate_sql_insert_data()
    print("\nGénération de données terminée!")

