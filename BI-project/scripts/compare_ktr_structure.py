#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare la structure de deux fichiers .ktr"""

import xml.etree.ElementTree as ET
import sys

def get_step_info(ktr_file, step_name):
    """Extrait les informations d'une étape spécifique"""
    try:
        tree = ET.parse(ktr_file)
        root = tree.getroot()
        
        for step in root.findall('.//step'):
            name_elem = step.find('name')
            if name_elem is not None and name_elem.text == step_name:
                type_elem = step.find('type')
                return {
                    'name': name_elem.text,
                    'type': type_elem.text if type_elem is not None else None,
                    'xml': ET.tostring(step, encoding='unicode')
                }
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

if __name__ == '__main__':
    file1 = 'pentaho/transformations/05_Load_Consumption_DM.ktr'
    file2 = 'pentaho/transformations/08_Load_Rentabilite_DM.ktr'
    
    step_name = 'CSV file input'
    
    print(f"\n=== Comparaison de '{step_name}' ===")
    
    info1 = get_step_info(file1, step_name)
    info2 = get_step_info(file2, step_name)
    
    if info1 and info2:
        print(f"\nFichier 1 ({file1}):")
        print(f"  Type: {info1['type']}")
        print(f"\nFichier 2 ({file2}):")
        print(f"  Type: {info2['type']}")
        
        # Comparer les éléments clés
        tree1 = ET.fromstring(info1['xml'])
        tree2 = ET.fromstring(info2['xml'])
        
        # Vérifier les éléments file
        file1_elem = tree1.find('file')
        file2_elem = tree2.find('file')
        
        if file1_elem is not None and file2_elem is not None:
            name1 = file1_elem.find('name')
            name2 = file2_elem.find('name')
            print(f"\nFile name 1: {name1.text if name1 is not None else 'None'}")
            print(f"File name 2: {name2.text if name2 is not None else 'None'}")
        
        # Compter les champs
        fields1 = tree1.findall('field')
        fields2 = tree2.findall('field')
        print(f"\nNombre de champs 1: {len(fields1)}")
        print(f"Nombre de champs 2: {len(fields2)}")
    else:
        print("Etape non trouvee dans un des fichiers")






