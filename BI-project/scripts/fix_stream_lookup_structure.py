"""
Script pour corriger la structure XML des étapes StreamLookup
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def fix_stream_lookup_structure(step):
    """Corrige la structure XML d'une étape StreamLookup"""
    # Supprimer les éléments qui ne sont pas pour StreamLookup
    for elem in ['connection', 'schema', 'table', 'orderby', 'fail_on_multiple', 'eat_row_on_failure']:
        old_elem = step.find(elem)
        if old_elem is not None:
            step.remove(old_elem)
    
    # Récupérer les clés et valeurs de l'ancienne structure
    keys = step.findall('.//key')
    values = step.findall('.//value')
    
    # Supprimer les anciennes structures key/value
    for key in keys:
        parent = key.getparent() if hasattr(key, 'getparent') else None
        if parent is not None:
            parent.remove(key)
    
    for value in values:
        parent = value.getparent() if hasattr(value, 'getparent') else None
        if parent is not None:
            parent.remove(value)
    
    # Créer la structure StreamLookup correcte
    lookup_elem = ET.Element('lookup')
    
    # Nom de l'étape source (Table Input)
    step_name = step.find('name').text
    source_step_name = f'Table input - {step_name.replace("Lookup ", "")}'
    ET.SubElement(lookup_elem, 'step').text = source_step_name
    
    # Clés
    keys_elem = ET.SubElement(lookup_elem, 'keys')
    if keys:
        for key in keys:
            key_name = key.find('name').text if key.find('name') is not None else ''
            key_field = key.find('field').text if key.find('field') is not None else key_name
            
            key_item = ET.SubElement(keys_elem, 'key')
            ET.SubElement(key_item, 'name').text = key_field
            ET.SubElement(key_item, 'field').text = key_field
            ET.SubElement(key_item, 'name2').text = key_field
    
    # Valeurs
    values_elem = ET.SubElement(lookup_elem, 'value')
    if values:
        for value in values:
            value_name = value.find('name').text if value.find('name') is not None else ''
            value_rename = value.find('rename').text if value.find('rename') is not None else value_name
            
            value_item = ET.SubElement(values_elem, 'name')
            value_item.text = value_rename
    
    # Options StreamLookup
    ET.SubElement(step, 'memory_preserve').text = 'N'
    ET.SubElement(step, 'sorted_list').text = 'N'
    ET.SubElement(step, 'integer_pair').text = 'N'
    
    # Insérer lookup après partitioning
    partitioning = step.find('partitioning')
    if partitioning is not None:
        step.insert(list(step).index(partitioning) + 1, lookup_elem)
    else:
        step.insert(0, lookup_elem)
    
    return step

def fix_file(file_path):
    """Corrige un fichier de transformation"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Trouver toutes les étapes StreamLookup
        steps = root.findall('.//step')
        stream_lookups = [s for s in steps if s.find('type') is not None and s.find('type').text == 'StreamLookup']
        
        if not stream_lookups:
            return False
        
        modified = False
        for lookup in stream_lookups:
            fix_stream_lookup_structure(lookup)
            modified = True
        
        if modified:
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            return True
        return False
        
    except Exception as e:
        print(f"  ERREUR: {e}")
        import traceback
        traceback.print_exc()
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
    
    print("Correction de la structure XML des StreamLookup...\n")
    
    for filename in files_to_fix:
        file_path = transformations_dir / filename
        if file_path.exists():
            print(f"Traitement de {filename}...")
            if fix_file(file_path):
                print(f"  OK: Structure corrigee")
            else:
                print(f"  Aucune modification necessaire")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")

if __name__ == '__main__':
    main()

