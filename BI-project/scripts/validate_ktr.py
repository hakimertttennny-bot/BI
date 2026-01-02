#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script pour valider la structure XML des fichiers .ktr"""

import xml.etree.ElementTree as ET
import sys
from pathlib import Path

def validate_ktr(file_path):
    """Valide un fichier .ktr et affiche les problèmes"""
    print(f"\n=== Validation de {file_path} ===")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print("[OK] XML valide")
        
        # Vérifier les étapes
        steps = root.findall('.//step')
        print(f"[OK] Nombre d'etapes: {len(steps)}")
        
        errors = []
        warnings = []
        
        # Vérifier chaque StreamLookup
        for step in steps:
            step_name = step.find('name')
            step_type = step.find('type')
            
            if step_name is not None and step_type is not None:
                name = step_name.text
                stype = step_type.text
                
                if stype == 'StreamLookup':
                    lookup = step.find('lookup')
                    if lookup is None:
                        errors.append(f"{name} - Pas de section <lookup>")
                    else:
                        step_elem = lookup.find('step')
                        keys = lookup.find('keys')
                        value = lookup.find('value')
                        
                        if step_elem is None:
                            errors.append(f"{name} - Pas de <step> dans <lookup>")
                        elif step_elem.text is None or step_elem.text.strip() == '':
                            errors.append(f"{name} - <step> est vide")
                        else:
                            print(f"[OK] {name} - step: {step_elem.text}")
                        
                        if keys is None:
                            errors.append(f"{name} - Pas de <keys> dans <lookup>")
                        else:
                            key_list = keys.findall('key')
                            if len(key_list) == 0:
                                errors.append(f"{name} - Aucune <key> dans <keys>")
                            else:
                                print(f"[OK] {name} - {len(key_list)} cle(s) definie(s)")
                        
                        if value is None:
                            errors.append(f"{name} - Pas de <value> dans <lookup>")
                        else:
                            print(f"[OK] {name} - <value> present")
                
                elif stype == 'CsvInput':
                    filename = step.find('filename')
                    fields = step.find('fields')
                    if filename is None or (filename.text is None or filename.text.strip() == ''):
                        warnings.append(f"{name} - Pas de nom de fichier defini")
                    if fields is None or len(fields.findall('field')) == 0:
                        warnings.append(f"{name} - Aucun champ defini")
        
        if errors:
            print("\n[ERREURS]:")
            for err in errors:
                print(f"  - {err}")
        
        if warnings:
            print("\n[WARNINGS]:")
            for warn in warnings:
                print(f"  - {warn}")
        
        if not errors and not warnings:
            print("\n[OK] Validation terminee - Aucun probleme detecte")
        elif errors:
            print(f"\n[ERREUR] {len(errors)} erreur(s) trouvee(s)")
        else:
            print(f"\n[OK] Validation terminee - {len(warnings)} avertissement(s)")
        return True
        
    except ET.ParseError as e:
        print(f"✗ ERREUR XML: {e}")
        return False
    except Exception as e:
        print(f"✗ ERREUR: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'pentaho/transformations/08_Load_Rentabilite_DM.ktr'
    
    validate_ktr(file_path)

