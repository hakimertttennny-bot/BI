#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige les positions GUI pour eviter les superpositions"""

import xml.etree.ElementTree as ET

def fix_gui_positions(ktr_file):
    """Corrige les positions GUI des etapes"""
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    steps = root.findall('.//step')
    x_start = 64
    y_start = 64
    x_spacing = 128
    
    # Pour 03_Extract_MySQL_Operational, organiser en 2 lignes
    if '03_Extract_MySQL_Operational' in ktr_file:
        x_pos = x_start
        y_pos = y_start
        items_per_row = 7
        
        for i, step in enumerate(steps):
            gui_elem = step.find('GUI')
            if gui_elem is None:
                gui_elem = ET.SubElement(step, 'GUI')
            
            xloc = gui_elem.find('xloc')
            yloc = gui_elem.find('yloc')
            draw = gui_elem.find('draw')
            
            if xloc is None:
                xloc = ET.SubElement(gui_elem, 'xloc')
            if yloc is None:
                yloc = ET.SubElement(gui_elem, 'yloc')
            if draw is None:
                draw = ET.SubElement(gui_elem, 'draw')
            
            # Nouvelle ligne apres items_per_row etapes
            if i > 0 and i % items_per_row == 0:
                y_pos += 128
                x_pos = x_start
            
            xloc.text = str(x_pos)
            yloc.text = str(y_pos)
            draw.text = 'Y'
            
            x_pos += x_spacing
    else:
        # Pour les autres fichiers, ligne horizontale simple
        x_pos = x_start
        y_pos = y_start
        
        for step in steps:
            gui_elem = step.find('GUI')
            if gui_elem is None:
                gui_elem = ET.SubElement(step, 'GUI')
            
            xloc = gui_elem.find('xloc')
            yloc = gui_elem.find('yloc')
            draw = gui_elem.find('draw')
            
            if xloc is None:
                xloc = ET.SubElement(gui_elem, 'xloc')
            if yloc is None:
                yloc = ET.SubElement(gui_elem, 'yloc')
            if draw is None:
                draw = ET.SubElement(gui_elem, 'draw')
            
            xloc.text = str(x_pos)
            yloc.text = str(y_pos)
            draw.text = 'Y'
            
            x_pos += x_spacing
    
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print(f"OK: {ktr_file} - Positions GUI corrigees")

def main():
    files = [
        'pentaho/transformations/01_Extract_JSON_Consumption.ktr',
        'pentaho/transformations/02_Extract_CSV_Environmental.ktr',
        'pentaho/transformations/03_Extract_MySQL_Operational.ktr'
    ]
    
    for ktr_file in files:
        fix_gui_positions(ktr_file)
    
    print("\nTous les fichiers ont ete corriges!")

if __name__ == '__main__':
    main()






