#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger complètement 02_Extract_CSV_Environmental.ktr
en copiant exactement la structure de 04_Transform_Consumption.ktr
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Retourne une chaîne XML formatée."""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

# Lire le fichier source qui fonctionne
tree_working = ET.parse('pentaho/transformations/04_Transform_Consumption.ktr')
root_working = tree_working.getroot()

# Lire le fichier à corriger
tree = ET.parse('pentaho/transformations/02_Extract_CSV_Environmental.ktr')
root = tree.getroot()

# Trouver l'étape CSVInput qui fonctionne
csv_input_working = None
for step in root_working.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'CSV file input':
        csv_input_working = step
        break

# Trouver l'étape SelectValues qui fonctionne
select_values_working = None
for step in root_working.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'Select values':
        select_values_working = step
        break

if csv_input_working is None or select_values_working is None:
    print("ERREUR: Impossible de trouver les étapes de référence")
    exit(1)

# Trouver et remplacer l'étape CSVInput
csv_input_to_replace = None
for step in root.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'CSV file input':
        csv_input_to_replace = step
        break

if csv_input_to_replace is not None:
    # Créer une nouvelle étape basée sur celle qui fonctionne
    new_csv_input = ET.fromstring(ET.tostring(csv_input_working, encoding='utf-8'))
    
    # Modifier le nom du fichier
    file_elem = new_csv_input.find('file')
    if file_elem is not None:
        name_elem = file_elem.find('name')
        if name_elem is not None:
            name_elem.text = '${Internal.Transformation.Filename.Directory}/data/source/environmental_*.csv'
    
    # Modifier les champs pour correspondre aux 5 champs environnementaux
    # Supprimer tous les champs existants
    for field in new_csv_input.findall('field'):
        new_csv_input.remove(field)
    
    # Ajouter les 5 champs environnementaux
    fields_data = [
        ('id_region', 'String', 'both'),
        ('id_batiment', 'String', 'both'),
        ('date_rapport', 'String', 'both'),
        ('emission_CO2_kg', 'Number', 'none'),
        ('taux_recyclage', 'Number', 'none'),
    ]
    
    for field_name, field_type, trim_type in fields_data:
        field = ET.SubElement(new_csv_input, 'field')
        ET.SubElement(field, 'name').text = field_name
        ET.SubElement(field, 'type').text = field_type
        ET.SubElement(field, 'format')
        ET.SubElement(field, 'currency')
        if field_type == 'Number':
            ET.SubElement(field, 'decimal').text = '.'
        else:
            ET.SubElement(field, 'decimal')
        ET.SubElement(field, 'group')
        ET.SubElement(field, 'trim_type').text = trim_type
        ET.SubElement(field, 'length').text = '-1'
        ET.SubElement(field, 'precision').text = '-1'
    
    # Modifier la description
    desc_elem = new_csv_input.find('description')
    if desc_elem is not None:
        desc_elem.text = 'Lecture des fichiers CSV environnementaux depuis le dossier source'
    
    # Modifier la position GUI
    gui_elem = new_csv_input.find('GUI')
    if gui_elem is not None:
        xloc_elem = gui_elem.find('xloc')
        yloc_elem = gui_elem.find('yloc')
        if xloc_elem is not None:
            xloc_elem.text = '496'
        if yloc_elem is not None:
            yloc_elem.text = '160'
    
    # Remplacer l'ancienne étape
    # Trouver le parent en parcourant l'arbre
    for parent in root.iter():
        if csv_input_to_replace in list(parent):
            parent.remove(csv_input_to_replace)
            parent.append(new_csv_input)
            break
    print("OK: Etape CSVInput remplacee")

# Trouver et remplacer l'étape SelectValues
select_values_to_replace = None
for step in root.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'Select values':
        select_values_to_replace = step
        break

if select_values_to_replace is not None:
    # Créer une nouvelle étape basée sur celle qui fonctionne
    new_select_values = ET.fromstring(ET.tostring(select_values_working, encoding='utf-8'))
    
    # Modifier la description
    desc_elem = new_select_values.find('description')
    if desc_elem is not None:
        desc_elem.text = 'Sélection et renommage des champs'
    
    # Modifier les champs dans <select>
    select_elem = new_select_values.find('select')
    if select_elem is not None:
        # Supprimer tous les champs existants
        for field in select_elem.findall('field'):
            select_elem.remove(field)
        
        # Ajouter les 5 champs environnementaux
        fields_data = [
            ('id_region', 'String'),
            ('id_batiment', 'String'),
            ('date_rapport', 'String'),
            ('emission_CO2_kg', 'Number'),
            ('taux_recyclage', 'Number'),
        ]
        
        for field_name, field_type in fields_data:
            field = ET.SubElement(select_elem, 'field')
            ET.SubElement(field, 'name').text = field_name
            ET.SubElement(field, 'rename').text = field_name
            ET.SubElement(field, 'default')
            ET.SubElement(field, 'type').text = field_type
            ET.SubElement(field, 'length').text = '-1'
            ET.SubElement(field, 'precision').text = '-1'
            ET.SubElement(field, 'replace')
    
    # Modifier la position GUI
    gui_elem = new_select_values.find('GUI')
    if gui_elem is not None:
        xloc_elem = gui_elem.find('xloc')
        yloc_elem = gui_elem.find('yloc')
        if xloc_elem is not None:
            xloc_elem.text = '656'
        if yloc_elem is not None:
            yloc_elem.text = '160'
    
    # Remplacer l'ancienne étape
    # Trouver le parent en parcourant l'arbre
    for parent in root.iter():
        if select_values_to_replace in list(parent):
            parent.remove(select_values_to_replace)
            parent.append(new_select_values)
            break
    print("OK: Etape SelectValues remplacee")

# Sauvegarder le fichier
tree.write('pentaho/transformations/02_Extract_CSV_Environmental.ktr', encoding='utf-8', xml_declaration=True)
print("OK: Fichier sauvegarde")

