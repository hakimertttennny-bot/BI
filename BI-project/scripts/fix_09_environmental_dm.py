#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige la transformation 09_Load_Environmental_DM.ktr"""

import xml.etree.ElementTree as ET
import sys

def fix_streamlookup(step_elem, lookup_step_name, key_field, value_field):
    """Corrige la configuration d'un StreamLookup"""
    # Supprimer les anciens éléments
    for elem in step_elem.findall('from'):
        step_elem.remove(elem)
    for elem in step_elem.findall('input_sorted'):
        step_elem.remove(elem)
    for elem in step_elem.findall('preserve_memory'):
        step_elem.remove(elem)
    for elem in step_elem.findall('sorted_list'):
        step_elem.remove(elem)
    for elem in step_elem.findall('integer_pair'):
        step_elem.remove(elem)
    
    # Trouver ou créer l'élément lookup
    lookup_elem = step_elem.find('lookup')
    if lookup_elem is None:
        lookup_elem = ET.SubElement(step_elem, 'lookup')
    else:
        # Nettoyer l'ancien contenu
        lookup_elem.clear()
    
    # Ajouter step
    step_name_elem = ET.SubElement(lookup_elem, 'step')
    step_name_elem.text = lookup_step_name
    
    # Ajouter keys
    keys_elem = ET.SubElement(lookup_elem, 'keys')
    key_elem = ET.SubElement(keys_elem, 'key')
    name_elem = ET.SubElement(key_elem, 'name')
    name_elem.text = key_field
    field_elem = ET.SubElement(key_elem, 'field')
    field_elem.text = key_field
    name2_elem = ET.SubElement(key_elem, 'name2')
    name2_elem.text = key_field
    
    # Ajouter value
    value_elem = ET.SubElement(lookup_elem, 'value')
    name_elem = ET.SubElement(value_elem, 'name')
    name_elem.text = value_field
    
    # Ajouter les éléments manquants à la fin
    memory_preserve = ET.SubElement(step_elem, 'memory_preserve')
    memory_preserve.text = 'N'
    sorted_list = ET.SubElement(step_elem, 'sorted_list')
    sorted_list.text = 'N'
    integer_pair = ET.SubElement(step_elem, 'integer_pair')
    integer_pair.text = 'N'

def fix_csvinput(step_elem):
    """Corrige le CSVInput"""
    # Changer le type
    type_elem = step_elem.find('type')
    if type_elem is not None:
        type_elem.text = 'CSVInput'
    
    # Supprimer les anciens éléments
    for elem in ['filename', 'filename_field', 'rownum_field', 'include_filename', 
                 'buffer_size', 'lazy_conversion', 'add_filename_result', 'parallel',
                 'newline_possible', 'format', 'encoding']:
        for child in step_elem.findall(elem):
            step_elem.remove(child)
    
    # Ajouter l'élément file
    file_elem = step_elem.find('file')
    if file_elem is None:
        file_elem = ET.SubElement(step_elem, 'file')
    
    # Nettoyer et ajouter les sous-éléments
    file_elem.clear()
    name_elem = ET.SubElement(file_elem, 'name')
    name_elem.text = '${Internal.Transformation.Filename.Directory}/data/transformed/environmental_transformed.csv'
    ET.SubElement(file_elem, 'filemask')
    ET.SubElement(file_elem, 'exclude_filemask')
    file_required = ET.SubElement(file_elem, 'file_required')
    file_required.text = 'N'
    include_subfolders = ET.SubElement(file_elem, 'include_subfolders')
    include_subfolders.text = 'N'
    
    # Ajouter les champs
    fields_elem = step_elem.find('fields')
    if fields_elem is not None:
        step_elem.remove(fields_elem)
    
    # Champs attendus du CSV transformé
    fields = [
        ('id_region', 'String'),
        ('id_batiment', 'String'),
        ('date_rapport', 'String'),
        ('emission_CO2_kg', 'Number'),
        ('taux_recyclage', 'Number'),
        ('emission_CO2_tonnes', 'Number')
    ]
    
    for field_name, field_type in fields:
        field_elem = ET.SubElement(step_elem, 'field')
        name_elem = ET.SubElement(field_elem, 'name')
        name_elem.text = field_name
        type_elem = ET.SubElement(field_elem, 'type')
        type_elem.text = field_type
        ET.SubElement(field_elem, 'format')
        ET.SubElement(field_elem, 'currency')
        decimal_elem = ET.SubElement(field_elem, 'decimal')
        if field_type == 'Number':
            decimal_elem.text = '.'
        ET.SubElement(field_elem, 'group')
        trim_type = ET.SubElement(field_elem, 'trim_type')
        trim_type.text = 'both' if field_type == 'String' else 'none'
        length = ET.SubElement(field_elem, 'length')
        length.text = '-1'
        precision = ET.SubElement(field_elem, 'precision')
        precision.text = '-1'
    
    # Ajouter les paramètres CSV
    separator = ET.SubElement(step_elem, 'separator')
    separator.text = ';'
    enclosure = ET.SubElement(step_elem, 'enclosure')
    enclosure.text = '"'
    ET.SubElement(step_elem, 'escape')
    header = ET.SubElement(step_elem, 'header')
    header.text = 'true'
    footer = ET.SubElement(step_elem, 'footer')
    footer.text = 'false'
    wiped = ET.SubElement(step_elem, 'wiped')
    wiped.text = 'false'
    lazyConversion = ET.SubElement(step_elem, 'lazyConversion')
    lazyConversion.text = 'false'

def fix_table_input(step_elem):
    """Ajoute schema aux Table Input"""
    schema_elem = step_elem.find('schema')
    if schema_elem is None:
        # Insérer après connection
        connection_elem = step_elem.find('connection')
        if connection_elem is not None:
            schema_elem = ET.SubElement(step_elem, 'schema')
            schema_elem.text = ''
            # Réorganiser pour mettre schema après connection
            step_elem.remove(schema_elem)
            idx = list(step_elem).index(connection_elem)
            step_elem.insert(idx + 1, schema_elem)

def fix_hops(root):
    """Active les hops entre Table Input et StreamLookup"""
    order_elem = root.find('order')
    if order_elem is None:
        return
    
    # Mapping des hops à activer
    hops_to_enable = [
        ('Table input - Lookup Region', 'Lookup Region'),
        ('Table input - Lookup Batiment', 'Lookup Batiment'),
        ('Table input - Lookup Temps', 'Lookup Temps'),
        ('CSV file input', 'Lookup Region'),
        ('Lookup Region', 'Lookup Batiment'),
        ('Lookup Batiment', 'Lookup Temps'),
        ('Lookup Temps', 'Table output')
    ]
    
    for hop in order_elem.findall('hop'):
        from_elem = hop.find('from')
        to_elem = hop.find('to')
        if from_elem is not None and to_elem is not None:
            from_name = from_elem.text
            to_name = to_elem.text
            if (from_name, to_name) in hops_to_enable:
                enabled_elem = hop.find('enabled')
                if enabled_elem is not None:
                    enabled_elem.text = 'Y'

def main():
    ktr_file = 'pentaho/transformations/09_Load_Environmental_DM.ktr'
    
    print(f"Lecture de {ktr_file}...")
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    # Trouver toutes les étapes
    steps = {}
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None:
            steps[name_elem.text] = step
    
    # Corriger CSVInput
    if 'CSV file input' in steps:
        print("Correction du CSVInput...")
        fix_csvinput(steps['CSV file input'])
    
    # Corriger StreamLookup
    print("Correction des StreamLookup...")
    if 'Lookup Region' in steps:
        fix_streamlookup(steps['Lookup Region'], 'Table input - Lookup Region', 'id_region', 'id_region_sk')
    if 'Lookup Batiment' in steps:
        fix_streamlookup(steps['Lookup Batiment'], 'Table input - Lookup Batiment', 'id_batiment', 'id_batiment_sk')
    if 'Lookup Temps' in steps:
        fix_streamlookup(steps['Lookup Temps'], 'Table input - Lookup Temps', 'date_rapport', 'id_temps_sk')
    
    # Corriger Table Input
    print("Correction des Table Input...")
    for name in ['Table input - Lookup Region', 'Table input - Lookup Batiment', 'Table input - Lookup Temps']:
        if name in steps:
            fix_table_input(steps[name])
    
    # Activer les hops
    print("Activation des hops...")
    fix_hops(root)
    
    # Sauvegarder
    print(f"Ecriture de {ktr_file}...")
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: Fichier corrige avec succes!")

if __name__ == '__main__':
    main()

