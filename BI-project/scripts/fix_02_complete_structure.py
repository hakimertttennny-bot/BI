#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige completement la structure de 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

def fix_csvinput_step(step_elem):
    """Corrige completement le CSVInput"""
    # Trouver GUI pour inserer avant
    gui_elem = step_elem.find('GUI')
    gui_index = list(step_elem).index(gui_elem) if gui_elem is not None else len(list(step_elem))
    
    # Supprimer les anciens buffer_size, format, encoding s'ils existent
    for tag in ['buffer_size', 'format', 'encoding']:
        elem = step_elem.find(tag)
        if elem is not None:
            step_elem.remove(elem)
    
    # Ajouter buffer_size avant GUI
    buffer_size = ET.Element('buffer_size')
    buffer_size.text = '50000'
    step_elem.insert(gui_index, buffer_size)
    gui_index += 1
    
    # Ajouter format avant GUI
    format_elem = ET.Element('format')
    format_elem.text = ''
    step_elem.insert(gui_index, format_elem)
    gui_index += 1
    
    # Ajouter encoding avant GUI
    encoding_elem = ET.Element('encoding')
    encoding_elem.text = ''
    step_elem.insert(gui_index, encoding_elem)

def main():
    ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'
    
    print(f"Lecture de {ktr_file}...")
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    # Trouver CSVInput
    csv_step = None
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None and name_elem.text == 'CSV file input':
            csv_step = step
            break
    
    if csv_step is not None:
        print("Correction du CSVInput...")
        fix_csvinput_step(csv_step)
    
    print(f"Ecriture de {ktr_file}...")
    ET.indent(tree, space='  ')
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: Structure corrigee!")

if __name__ == '__main__':
    main()






