#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige tous les champs manquants dans CSVInput - version complete"""

import xml.etree.ElementTree as ET

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
    
    if csv_step is None:
        print("ERREUR: CSVInput step non trouve!")
        return
    
    # Trouver l'index de GUI
    gui_elem = csv_step.find('GUI')
    gui_index = list(csv_step).index(gui_elem) if gui_elem is not None else len(list(csv_step))
    
    # Elements a ajouter/verifier avec valeurs par defaut
    elements_to_add = {
        'buffer_size': '50000',
        'format': '',
        'encoding': ''
    }
    
    for elem_name, default_value in elements_to_add.items():
        elem = csv_step.find(elem_name)
        if elem is None:
            # Creer l'element avant GUI
            elem = ET.Element(elem_name)
            elem.text = default_value
            csv_step.insert(gui_index, elem)
            gui_index += 1
        elif elem.text is None or elem.text == '':
            elem.text = default_value
    
    print(f"Ecriture de {ktr_file}...")
    ET.indent(tree, space='  ')
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: Tous les champs ajoutes!")

if __name__ == '__main__':
    main()






