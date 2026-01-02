"""
Script pour corriger toutes les étapes DatabaseLookup avec la structure complète
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def fix_database_lookup_steps(file_path):
    """Corrige toutes les étapes DatabaseLookup dans un fichier"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        modified = False
        steps = root.findall('.//step')
        
        for step in steps:
            step_type = step.find('type')
            if step_type is not None and step_type.text == 'DatabaseLookup':
                # Vérifier si cluster_schema et remotesteps existent
                cluster_schema = step.find('cluster_schema')
                remotesteps = step.find('remotesteps')
                
                if cluster_schema is None:
                    # Ajouter cluster_schema avant GUI
                    gui = step.find('GUI')
                    if gui is not None:
                        cluster_elem = ET.Element('cluster_schema')
                        step.insert(list(step).index(gui), cluster_elem)
                        modified = True
                
                if remotesteps is None:
                    # Ajouter remotesteps avant GUI
                    gui = step.find('GUI')
                    if gui is not None:
                        remote_elem = ET.Element('remotesteps')
                        input_elem = ET.SubElement(remote_elem, 'input')
                        output_elem = ET.SubElement(remote_elem, 'output')
                        step.insert(list(step).index(gui), remote_elem)
                        modified = True
        
        if modified:
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            return True
        return False
        
    except Exception as e:
        print(f"  ERREUR: {e}")
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
            if fix_database_lookup_steps(file_path):
                print(f"  OK: {filename} corrige")
            else:
                print(f"  Aucune modification necessaire pour {filename}")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")

if __name__ == '__main__':
    main()

