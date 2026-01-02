#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification finale de 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'

tree = ET.parse(ktr_file)

# Trouver CSVInput
csv_step = None
for step in tree.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'CSV file input':
        csv_step = step
        break

if csv_step is not None:
    print("CSVInput - Verification des champs:")
    buffer_size = csv_step.find('buffer_size')
    print(f"  - buffer_size: {buffer_size.text if buffer_size is not None and buffer_size.text else 'MANQUANT'}")
    
    format_elem = csv_step.find('format')
    print(f"  - format: {'OK' if format_elem is not None else 'MANQUANT'}")
    
    encoding_elem = csv_step.find('encoding')
    print(f"  - encoding: {'OK' if encoding_elem is not None else 'MANQUANT'}")
    
    # Verifier l'ordre (buffer_size, format, encoding doivent etre avant GUI)
    elements = list(csv_step)
    gui_index = None
    buffer_index = None
    format_index = None
    encoding_index = None
    
    for i, elem in enumerate(elements):
        if elem.tag == 'GUI':
            gui_index = i
        elif elem.tag == 'buffer_size':
            buffer_index = i
        elif elem.tag == 'format':
            format_index = i
        elif elem.tag == 'encoding':
            encoding_index = i
    
    if gui_index is not None:
        print(f"\nOrdre des elements (index GUI: {gui_index}):")
        if buffer_index is not None:
            print(f"  - buffer_size: index {buffer_index} {'OK' if buffer_index < gui_index else 'APRES GUI - ERREUR'}")
        if format_index is not None:
            print(f"  - format: index {format_index} {'OK' if format_index < gui_index else 'APRES GUI - ERREUR'}")
        if encoding_index is not None:
            print(f"  - encoding: index {encoding_index} {'OK' if encoding_index < gui_index else 'APRES GUI - ERREUR'}")

print("\nVerification terminee!")






