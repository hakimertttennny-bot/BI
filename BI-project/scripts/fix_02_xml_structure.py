#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige la structure XML de 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

def main():
    ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'
    
    print(f"Lecture de {ktr_file}...")
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    # Trouver CSVInput
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None and name_elem.text == 'CSV file input':
            # Verifier si les elements sont mal places
            gui_elem = step.find('GUI')
            file_elem = step.find('file')
            
            # Si file est apres GUI, le deplacer avant
            if gui_elem is not None and file_elem is not None:
                gui_index = list(step).index(gui_elem)
                file_index = list(step).index(file_elem)
                
                if file_index > gui_index:
                    # Deplacer file avant GUI
                    step.remove(file_elem)
                    step.insert(gui_index, file_elem)
            
            # Reorganiser: file, fields, separator, etc. avant GUI
            elements_order = ['file', 'field', 'separator', 'enclosure', 'escape', 
                            'header', 'footer', 'wiped', 'lazyConversion']
            
            # Trouver l'index de GUI
            gui_elem = step.find('GUI')
            if gui_elem is not None:
                gui_index = list(step).index(gui_elem)
                
                # Deplacer tous les elements avant GUI
                for tag in elements_order:
                    for elem in step.findall(tag):
                        if list(step).index(elem) > gui_index:
                            step.remove(elem)
                            step.insert(gui_index, elem)
                            gui_index += 1
    
    # Corriger Filter rows
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None and name_elem.text == 'Filter rows':
            # Reorganiser compare et conditions
            gui_elem = step.find('GUI')
            compare_elem = step.find('compare')
            conditions_elem = step.find('conditions')
            
            if gui_elem is not None:
                gui_index = list(step).index(gui_elem)
                
                # Deplacer compare et conditions avant GUI
                if compare_elem is not None and list(step).index(compare_elem) > gui_index:
                    step.remove(compare_elem)
                    step.insert(gui_index, compare_elem)
                    gui_index += 1
                
                if conditions_elem is not None and list(step).index(conditions_elem) > gui_index:
                    step.remove(conditions_elem)
                    step.insert(gui_index, conditions_elem)
    
    # Sauvegarder avec indentation
    print(f"Ecriture de {ktr_file}...")
    ET.indent(tree, space='  ')
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: Structure XML corrigee!")

if __name__ == '__main__':
    main()






