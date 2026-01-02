"""
Script pour corriger les étapes DatabaseLookup dans les fichiers .ktr
"""

import re
from pathlib import Path

def fix_database_lookup_in_file(file_path):
    """Corrige les étapes DatabaseLookup dans un fichier"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les étapes DatabaseLookup qui n'ont pas les balises complètes
    # On cherche les patterns où il y a </value> suivi directement de <GUI> sans cluster_schema et remotesteps
    pattern = r'(</value>)\s*(<GUI><xloc>.*?</GUI></step>)'
    
    replacement = r'\1\n    <cluster_schema />\n    <remotesteps>\n      <input>\n      </input>\n      <output>\n      </output>\n    </remotesteps>\n    \2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Si le contenu a changé, sauvegarder
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    # Fichiers avec DatabaseLookup
    files_to_fix = [
        '05_Load_Consumption_DM.ktr',
        '08_Load_Rentabilite_DM.ktr',
        '09_Load_Environmental_DM.ktr'
    ]
    
    for filename in files_to_fix:
        file_path = transformations_dir / filename
        if file_path.exists():
            print(f"Traitement de {filename}...")
            if fix_database_lookup_in_file(file_path):
                print(f"  OK: {filename} corrige")
            else:
                print(f"  Aucune modification necessaire pour {filename}")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")

if __name__ == '__main__':
    main()

