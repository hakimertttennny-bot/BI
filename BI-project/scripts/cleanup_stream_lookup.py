"""
Script pour nettoyer complètement les étapes StreamLookup
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re

def cleanup_stream_lookup(file_path):
    """Nettoie les étapes StreamLookup"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Supprimer les anciens éléments key et value qui sont en double
    # Pattern pour trouver les éléments key/value après </lookup>
    pattern = r'(</lookup>)(.*?)(<cluster_schema />)'
    
    def replace_func(match):
        lookup_end = match.group(1)
        middle = match.group(2)
        cluster = match.group(3)
        
        # Supprimer les anciens éléments <key> et <value> dans middle
        cleaned = re.sub(r'<key>.*?</key>', '', middle, flags=re.DOTALL)
        cleaned = re.sub(r'<value>.*?</value>', '', cleaned, flags=re.DOTALL)
        
        return lookup_end + cleaned + cluster
    
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    # Supprimer aussi les éléments connection, schema, table, orderby, fail_on_multiple, eat_row_on_failure qui restent
    elements_to_remove = [
        r'<connection>.*?</connection>',
        r'<schema />',
        r'<table>.*?</table>',
        r'<orderby />',
        r'<fail_on_multiple>.*?</fail_on_multiple>',
        r'<eat_row_on_failure>.*?</eat_row_on_failure>'
    ]
    
    for pattern in elements_to_remove:
        # Seulement dans les étapes StreamLookup
        new_content = re.sub(
            r'(<type>StreamLookup</type>.*?)(<lookup>)',
            lambda m: re.sub(pattern, '', m.group(1), flags=re.DOTALL) + m.group(2),
            new_content,
            flags=re.DOTALL
        )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    files_to_fix = [
        '05_Load_Consumption_DM.ktr',
        '08_Load_Rentabilite_DM.ktr',
        '09_Load_Environmental_DM.ktr'
    ]
    
    print("Nettoyage des etapes StreamLookup...\n")
    
    for filename in files_to_fix:
        file_path = transformations_dir / filename
        if file_path.exists():
            print(f"Traitement de {filename}...")
            if cleanup_stream_lookup(file_path):
                print(f"  OK: Fichier nettoye")
            else:
                print(f"  Aucune modification necessaire")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")

if __name__ == '__main__':
    main()

