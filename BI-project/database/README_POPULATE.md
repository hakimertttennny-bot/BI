# Guide de peuplement du Data Warehouse GreenCity

Ce guide explique comment peupler toutes les tables du Data Warehouse `greencity_dw`.

## Ordre d'exécution des scripts

Pour respecter les contraintes de clés étrangères, exécutez les scripts dans l'ordre suivant :

### 1. Dimensions de base (sans dépendances)

```sql
-- Dim_Type_Energie (3 enregistrements)
SOURCE database/05_init_dim_type_energie.sql;

-- Dim_Temps (peuple toutes les dates/heures de 2020 à 2030)
SOURCE database/04_populate_dim_temps.sql;
```

### 2. Toutes les dimensions des Data Marts

```sql
-- Peuple toutes les dimensions : Consommation, Rentabilité, Environnement
SOURCE database/08_populate_all_dimensions.sql;
```

Ce script insère :
- **Data Mart Consommation** : Dim_Region_Consommation (5), Dim_Batiment_Consommation (14), Dim_Client_Consommation (50), Dim_Compteur (60)
- **Data Mart Rentabilité** : Dim_Region_Rentabilite (5), Dim_Batiment_Rentabilite (14), Dim_Client_Rentabilite (50)
- **Data Mart Environnement** : Dim_Region_Environnement (5), Dim_Batiment_Environnement (14)

### 3. Tables de faits (optionnel)

```sql
-- Insère des données d'exemple dans les tables de faits
-- NOTE: Normalement, ces tables sont remplies par les processus ETL Pentaho
SOURCE database/09_populate_fact_tables.sql;
```

## Exécution via ligne de commande MySQL

```bash
# Depuis le répertoire racine du projet
mysql -u root -p greencity_dw < database/05_init_dim_type_energie.sql
mysql -u root -p greencity_dw < database/04_populate_dim_temps.sql
mysql -u root -p greencity_dw < database/08_populate_all_dimensions.sql
# Optionnel:
mysql -u root -p greencity_dw < database/09_populate_fact_tables.sql
```

## Exécution via MySQL Workbench / phpMyAdmin

1. Ouvrez chaque fichier SQL dans l'ordre indiqué ci-dessus
2. Sélectionnez la base de données `greencity_dw`
3. Exécutez chaque script dans l'ordre

## Vérification

Pour vérifier que toutes les tables ont été peuplées :

```sql
USE greencity_dw;

SELECT 'Dim_Region_Consommation' AS Table_Name, COUNT(*) AS Count FROM Dim_Region_Consommation
UNION ALL SELECT 'Dim_Batiment_Consommation', COUNT(*) FROM Dim_Batiment_Consommation
UNION ALL SELECT 'Dim_Client_Consommation', COUNT(*) FROM Dim_Client_Consommation
UNION ALL SELECT 'Dim_Compteur', COUNT(*) FROM Dim_Compteur
UNION ALL SELECT 'Dim_Temps', COUNT(*) FROM Dim_Temps
UNION ALL SELECT 'Dim_Region_Rentabilite', COUNT(*) FROM Dim_Region_Rentabilite
UNION ALL SELECT 'Dim_Batiment_Rentabilite', COUNT(*) FROM Dim_Batiment_Rentabilite
UNION ALL SELECT 'Dim_Client_Rentabilite', COUNT(*) FROM Dim_Client_Rentabilite
UNION ALL SELECT 'Dim_Type_Energie', COUNT(*) FROM Dim_Type_Energie
UNION ALL SELECT 'Dim_Region_Environnement', COUNT(*) FROM Dim_Region_Environnement
UNION ALL SELECT 'Dim_Batiment_Environnement', COUNT(*) FROM Dim_Batiment_Environnement;
```

## Résumé des données insérées

- **Régions** : 5 régions françaises (REG01 à REG05)
- **Bâtiments** : 14 bâtiments répartis sur les 5 régions
- **Clients** : 50 clients (mix Particulier/Entreprise/Administration)
- **Compteurs** : 60 compteurs (électricité, eau, gaz)
- **Type_Energie** : 3 types (électricité, eau, gaz)
- **Temps** : Toutes les heures de 2020-01-01 à 2030-12-31

## Notes importantes

1. Les scripts utilisent `ON DUPLICATE KEY UPDATE` pour éviter les erreurs si vous exécutez plusieurs fois
2. Les tables de faits sont normalement remplies par les processus ETL (Pentaho)
3. Le script `04_populate_dim_temps.sql` peut prendre quelques minutes à s'exécuter (beaucoup de données)
4. Les dimensions sont conçues pour supporter le SCD Type 2 (Slowly Changing Dimensions) avec `date_debut_validite` et `date_fin_validite`




