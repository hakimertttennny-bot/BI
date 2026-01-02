#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige tous les champs manquants dans CSVInput"""

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
    
    # Ajouter les elements manquants avec valeurs par defaut
    # buffer_size
    buffer_size = csv_step.find('buffer_size')
    if buffer_size is None:
        buffer_size = ET.SubElement(csv_step, 'buffer_size')
        buffer_size.text = '50000'
    elif buffer_size.text is None or buffer_size.text == '':
        buffer_size.text = '50000'
    
    # Reorganiser l'ordre des elements pour correspondre au format Pentaho
    # Ordre attendu: file, field(s), separator, enclosure, escape, header, footer, wiped, lazyConversion, buffer_size, etc.
    
    # Trouver l'index de GUI pour inserer avant
    gui_elem = csv_step.find('GUI')
    gui_index = list(csv_step).index(gui_elem) if gui_elem is not None else len(list(csv_step))
    
    # S'assurer que buffer_size est avant GUI
    if buffer_size is not None:
        current_index = list(csv_step).index(buffer_size)
        if current_index > gui_index:
            csv_step.remove(buffer_size)
            csv_step.insert(gui_index, buffer_size)
            gui_index += 1
    
    # Ajouter d'autres elements si necessaires
    # format (peut etre vide mais doit exister)
    format_elem = csv_step.find('format')
    if format_elem is None:
        format_elem = ET.SubElement(csv_step, 'format')
        format_elem.text = ''
    
    # encoding (peut etre vide mais doit exister)
    encoding_elem = csv_step.find('encoding')
    if encoding_elem is None:
        encoding_elem = ET.SubElement(csv_step, 'encoding')
        encoding_elem.text = ''
    
    # Reorganiser pour mettre format et encoding avant GUI
    if format_elem is not None:
        current_index = list(csv_step).index(format_elem)
        if current_index > gui_index:
            csv_step.remove(format_elem)
            csv_step.insert(gui_index, format_elem)
            gui_index += 1
    
    if encoding_elem is not None:
        current_index = list(csv_step).index(encoding_elem)
        if current_index > gui_index:
            csv_step.remove(encoding_elem)
            csv_step.insert(gui_index, encoding_elem)
    
    print(f"Ecriture de {ktr_file}...")
    ET.indent(tree, space='  ')
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: CSVInput corrige avec tous les champs!")

if __name__ == '__main__':
    main()






