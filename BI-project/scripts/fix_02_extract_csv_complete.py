#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige completement 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

def fix_csvinput(step_elem):
    """Corrige le CSVInput pour utiliser le format moderne"""
    # Changer le type
    type_elem = step_elem.find('type')
    if type_elem is not None:
        type_elem.text = 'CSVInput'
    
    # Supprimer les anciens elements
    for tag in ['filename', 'filename_field', 'rownum_field', 'include_filename',
                'separator', 'enclosure', 'header', 'buffer_size', 'lazy_conversion',
                'add_filename_result', 'parallel', 'newline_possible', 'format', 'encoding', 'fields']:
        for elem in step_elem.findall(tag):
            step_elem.remove(elem)
    
    # Ajouter file element
    file_elem = ET.SubElement(step_elem, 'file')
    name_elem = ET.SubElement(file_elem, 'name')
    name_elem.text = '${Internal.Transformation.Filename.Directory}/data/source/environmental_*.csv'
    ET.SubElement(file_elem, 'filemask')
    ET.SubElement(file_elem, 'exclude_filemask')
    file_required = ET.SubElement(file_elem, 'file_required')
    file_required.text = 'N'
    include_subfolders = ET.SubElement(file_elem, 'include_subfolders')
    include_subfolders.text = 'N'
    
    # Ajouter les champs
    fields_data = [
        ('id_region', 'String'),
        ('id_batiment', 'String'),
        ('date_rapport', 'String'),
        ('emission_CO2_kg', 'Number'),
        ('taux_recyclage', 'Number')
    ]
    
    for field_name, field_type in fields_data:
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
    
    # Ajouter parametres CSV
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

def fix_select_values(step_elem):
    """Corrige Select values pour inclure tous les champs"""
    # Trouver ou creer select
    select_elem = step_elem.find('select')
    if select_elem is None:
        select_elem = ET.SubElement(step_elem, 'select')
    else:
        # Nettoyer
        select_elem.clear()
    
    fields_data = [
        ('id_region', 'String'),
        ('id_batiment', 'String'),
        ('date_rapport', 'String'),
        ('emission_CO2_kg', 'Number'),
        ('taux_recyclage', 'Number')
    ]
    
    for field_name, field_type in fields_data:
        field_elem = ET.SubElement(select_elem, 'field')
        name_elem = ET.SubElement(field_elem, 'name')
        name_elem.text = field_name
        rename_elem = ET.SubElement(field_elem, 'rename')
        rename_elem.text = field_name
        ET.SubElement(field_elem, 'default')
        type_elem = ET.SubElement(field_elem, 'type')
        type_elem.text = field_type
        length = ET.SubElement(field_elem, 'length')
        length.text = '-1'
        precision = ET.SubElement(field_elem, 'precision')
        precision.text = '-1'
        ET.SubElement(field_elem, 'replace')
    
    # Meta et remove
    meta_elem = step_elem.find('meta')
    if meta_elem is None:
        ET.SubElement(step_elem, 'meta')
    remove_elem = step_elem.find('remove')
    if remove_elem is None:
        ET.SubElement(step_elem, 'remove')

def fix_filter_rows(step_elem):
    """Corrige Filter rows"""
    # Supprimer l'ancien compare
    compare_elem = step_elem.find('compare')
    if compare_elem is not None:
        step_elem.remove(compare_elem)
    
    # Creer le nouveau compare
    compare_elem = ET.SubElement(step_elem, 'compare')
    condition_elem = ET.SubElement(compare_elem, 'condition')
    value1 = ET.SubElement(condition_elem, 'value1')
    value1.text = 'date_rapport'
    value2 = ET.SubElement(condition_elem, 'value2')
    value2.text = 'invalid-date'
    condition = ET.SubElement(condition_elem, 'condition')
    condition.text = 'NOT EQUAL'
    
    # Conditions
    conditions_elem = step_elem.find('conditions')
    if conditions_elem is None:
        conditions_elem = ET.SubElement(step_elem, 'conditions')
    else:
        conditions_elem.clear()
    
    condition_elem = ET.SubElement(conditions_elem, 'condition')
    negated = ET.SubElement(condition_elem, 'negated')
    negated.text = 'false'
    leftvalue = ET.SubElement(condition_elem, 'leftvalue')
    leftvalue.text = 'date_rapport'
    function = ET.SubElement(condition_elem, 'function')
    function.text = '='
    rightvalue = ET.SubElement(condition_elem, 'rightvalue')
    rightvalue.text = 'invalid-date'
    leftvaluetype = ET.SubElement(condition_elem, 'leftvaluetype')
    leftvaluetype.text = 'String'
    rightvaluetype = ET.SubElement(condition_elem, 'rightvaluetype')
    rightvaluetype.text = 'String'

def fix_hops(root):
    """Active tous les hops"""
    order_elem = root.find('order')
    if order_elem is None:
        return
    
    for hop in order_elem.findall('hop'):
        enabled_elem = hop.find('enabled')
        if enabled_elem is not None:
            enabled_elem.text = 'Y'

def main():
    ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'
    
    print(f"Lecture de {ktr_file}...")
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    # Trouver toutes les etapes
    steps = {}
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None:
            steps[name_elem.text] = step
    
    # Corriger CSVInput
    if 'CSV file input' in steps:
        print("Correction du CSVInput...")
        fix_csvinput(steps['CSV file input'])
    
    # Corriger Select values
    if 'Select values' in steps:
        print("Correction du Select values...")
        fix_select_values(steps['Select values'])
    
    # Corriger Filter rows
    if 'Filter rows' in steps:
        print("Correction du Filter rows...")
        fix_filter_rows(steps['Filter rows'])
    
    # Activer les hops
    print("Activation des hops...")
    fix_hops(root)
    
    # Sauvegarder
    print(f"Ecriture de {ktr_file}...")
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: Fichier corrige avec succes!")

if __name__ == '__main__':
    main()






