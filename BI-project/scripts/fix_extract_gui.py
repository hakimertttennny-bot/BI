#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute les elements GUI manquants aux fichiers d'extraction"""

import xml.etree.ElementTree as ET
import sys

def add_gui_to_steps(root, x_start=64, y_start=64, x_spacing=128):
    """Ajoute les elements GUI a toutes les etapes"""
    steps = root.findall('.//step')
    x_pos = x_start
    y_pos = y_start
    
    for step in steps:
        # Verifier si GUI existe deja
        gui_elem = step.find('GUI')
        if gui_elem is None:
            # Creer GUI
            gui_elem = ET.SubElement(step, 'GUI')
            xloc = ET.SubElement(gui_elem, 'xloc')
            xloc.text = str(x_pos)
            yloc = ET.SubElement(gui_elem, 'yloc')
            yloc.text = str(y_pos)
            draw = ET.SubElement(gui_elem, 'draw')
            draw.text = 'Y'
        else:
            # Mettre a jour si necessaire
            xloc = gui_elem.find('xloc')
            yloc = gui_elem.find('yloc')
            draw = gui_elem.find('draw')
            
            if xloc is None:
                xloc = ET.SubElement(gui_elem, 'xloc')
                xloc.text = str(x_pos)
            else:
                xloc.text = str(x_pos)
            
            if yloc is None:
                yloc = ET.SubElement(gui_elem, 'yloc')
                yloc.text = str(y_pos)
            else:
                yloc.text = str(y_pos)
            
            if draw is None:
                draw = ET.SubElement(gui_elem, 'draw')
                draw.text = 'Y'
            else:
                draw.text = 'Y'
        
        x_pos += x_spacing

def main():
    files = [
        'pentaho/transformations/01_Extract_JSON_Consumption.ktr',
        'pentaho/transformations/03_Extract_MySQL_Operational.ktr'
    ]
    
    for ktr_file in files:
        print(f"Traitement de {ktr_file}...")
        try:
            tree = ET.parse(ktr_file)
            root = tree.getroot()
            
            # Ajouter GUI aux etapes
            add_gui_to_steps(root)
            
            # Sauvegarder
            tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
            print(f"OK: {ktr_file} corrige")
        except Exception as e:
            print(f"ERREUR avec {ktr_file}: {e}")
            sys.exit(1)
    
    print("Tous les fichiers ont ete corriges!")

if __name__ == '__main__':
    main()






