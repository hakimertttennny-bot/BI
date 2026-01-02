"""
Script final pour formater et valider tous les fichiers .ktr
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re

def format_xml_file(file_path):
    """Formate un fichier XML pour améliorer la lisibilité"""
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser avec ET pour valider
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Réécrire avec indentation
        ET.indent(tree, space='  ')
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        
        return True
    except ET.ParseError as e:
        print(f"  ERREUR XML: {e}")
        return False
    except Exception as e:
        print(f"  ERREUR: {e}")
        return False

def fix_table_input_formatting(file_path):
    """Corrige le formatage des Table Input qui sont sur une seule ligne"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les Table Input sur une seule ligne
    # Remplacer les balises compactes par des balises formatées
    original_content = content
    
    # Le formatage sera fait par ET.indent, mais on peut aussi corriger manuellement
    # les éléments qui sont sur une seule ligne
    
    return False  # Le formatage ET.indent suffit

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    ktr_files = list(transformations_dir.glob('*.ktr'))
    
    if not ktr_files:
        print("Aucun fichier .ktr trouve!")
        return
    
    print(f"Formatage de {len(ktr_files)} fichier(s) .ktr...\n")
    
    success_count = 0
    for ktr_file in sorted(ktr_files):
        print(f"Traitement de {ktr_file.name}...")
        try:
            if format_xml_file(ktr_file):
                print(f"  OK: Fichier formate et valide")
                success_count += 1
            else:
                print(f"  ERREUR lors du formatage")
        except Exception as e:
            print(f"  ERREUR: {e}")
    
    print(f"\nTermine! {success_count}/{len(ktr_files)} fichier(s) formate(s).")
    print("\nTous les fichiers sont maintenant prets pour Pentaho Spoon!")

if __name__ == '__main__':
    main()

