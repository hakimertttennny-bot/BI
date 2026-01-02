#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valide les fichiers d'extraction"""

import xml.etree.ElementTree as ET

files = [
    'pentaho/transformations/01_Extract_JSON_Consumption.ktr',
    'pentaho/transformations/02_Extract_CSV_Environmental.ktr',
    'pentaho/transformations/03_Extract_MySQL_Operational.ktr'
]

print("=== Validation des fichiers d'extraction ===\n")

for ktr_file in files:
    try:
        tree = ET.parse(ktr_file)
        root = tree.getroot()
        
        steps = root.findall('.//step')
        gui_steps = [s for s in steps if s.find('GUI') is not None]
        
        filename = ktr_file.split('/')[-1]
        print(f"{filename}:")
        print(f"  - Total etapes: {len(steps)}")
        print(f"  - Etapes avec GUI: {len(gui_steps)}")
        
        if len(steps) == len(gui_steps):
            print("  - OK: Toutes les etapes ont un element GUI")
        else:
            print(f"  - ATTENTION: {len(steps) - len(gui_steps)} etapes sans GUI")
        
        # Verifier la structure XML
        if root.tag == 'transformation':
            print("  - OK: Structure XML valide")
        else:
            print(f"  - ERREUR: Tag racine incorrect: {root.tag}")
        
        print()
    except Exception as e:
        print(f"{ktr_file}: ERREUR - {e}\n")

print("Validation terminee!")






