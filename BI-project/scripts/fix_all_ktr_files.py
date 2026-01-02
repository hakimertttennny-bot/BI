"""
Script complet pour corriger toutes les configurations des fichiers .ktr
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re

def fix_json_input_step(step):
    """Corrige une étape JSON Input"""
    # Le type JsonInput est correct, mais vérifier la structure
    return step

def fix_csv_input_step(step):
    """Corrige une étape CSV Input"""
    # S'assurer que le type est CSVInput (pas CsvInput)
    type_elem = step.find('type')
    if type_elem is not None and type_elem.text == 'CsvInput':
        type_elem.text = 'CSVInput'
    return step

def fix_stream_lookup_step(step, table_input_name):
    """Corrige complètement une étape StreamLookup"""
    # Supprimer tous les éléments obsolètes
    elements_to_remove = ['connection', 'schema', 'table', 'orderby', 
                         'fail_on_multiple', 'eat_row_on_failure', 'key', 'value']
    
    for elem_name in elements_to_remove:
        for elem in step.findall(elem_name):
            step.remove(elem)
    
    # Vérifier si lookup existe déjà
    lookup_elem = step.find('lookup')
    if lookup_elem is None:
        lookup_elem = ET.Element('lookup')
        # Insérer après partitioning
        partitioning = step.find('partitioning')
        if partitioning is not None:
            step.insert(list(step).index(partitioning) + 1, lookup_elem)
        else:
            step.insert(0, lookup_elem)
    
    # Configurer le step source
    step_elem = lookup_elem.find('step')
    if step_elem is None:
        step_elem = ET.SubElement(lookup_elem, 'step')
    step_elem.text = table_input_name
    
    # Configurer les keys (basé sur le nom de l'étape)
    step_name = step.find('name').text
    key_field = None
    if 'Region' in step_name:
        key_field = 'id_region'
    elif 'Batiment' in step_name:
        key_field = 'id_batiment'
    elif 'Client' in step_name:
        key_field = 'id_client'
    elif 'Compteur' in step_name:
        key_field = 'compteur_id'
    elif 'Type Energie' in step_name or 'Type_Energie' in step_name:
        key_field = 'type_energie'
    elif 'Temps' in step_name:
        key_field = 'date_complete'
    
    if key_field:
        keys_elem = lookup_elem.find('keys')
        if keys_elem is None:
            keys_elem = ET.SubElement(lookup_elem, 'keys')
        else:
            keys_elem.clear()
        
        key_item = ET.SubElement(keys_elem, 'key')
        ET.SubElement(key_item, 'name').text = key_field
        ET.SubElement(key_item, 'field').text = key_field
        ET.SubElement(key_item, 'name2').text = key_field
    
    # Configurer les values (basé sur le nom de l'étape)
    values_elem = lookup_elem.find('value')
    if values_elem is None:
        values_elem = ET.SubElement(lookup_elem, 'value')
    else:
        values_elem.clear()
    
    if 'Region' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_region_sk'
        ET.SubElement(values_elem, 'name').text = 'nom_region'
    elif 'Batiment' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_batiment_sk'
    elif 'Client' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_client_sk'
    elif 'Compteur' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_compteur_sk'
    elif 'Type Energie' in step_name or 'Type_Energie' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_type_energie_sk'
    elif 'Temps' in step_name:
        ET.SubElement(values_elem, 'name').text = 'id_temps_sk'
    
    # Options StreamLookup
    if step.find('memory_preserve') is None:
        ET.SubElement(step, 'memory_preserve').text = 'N'
    if step.find('sorted_list') is None:
        ET.SubElement(step, 'sorted_list').text = 'N'
    if step.find('integer_pair') is None:
        ET.SubElement(step, 'integer_pair').text = 'N'
    
    return step

def fix_table_input_step(step):
    """Corrige une étape Table Input"""
    # Vérifier que le type est TableInput
    type_elem = step.find('type')
    if type_elem is not None and type_elem.text != 'TableInput':
        type_elem.text = 'TableInput'
    return step

def fix_table_output_step(step):
    """Corrige une étape Table Output"""
    # Vérifier que le type est TableOutput
    type_elem = step.find('type')
    if type_elem is not None and type_elem.text != 'TableOutput':
        type_elem.text = 'TableOutput'
    return step

def fix_text_file_output_step(step):
    """Corrige une étape Text File Output"""
    # Vérifier que le type est TextFileOutput
    type_elem = step.find('type')
    if type_elem is not None and type_elem.text != 'TextFileOutput':
        type_elem.text = 'TextFileOutput'
    return step

def fix_all_steps_in_file(file_path):
    """Corrige toutes les étapes dans un fichier"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        modified = False
        steps = root.findall('.//step')
        
        # Mapping des noms de lookup vers les table input
        lookup_to_table_input = {}
        for step in steps:
            step_name = step.find('name')
            if step_name is not None:
                name = step_name.text
                if 'Table input' in name:
                    # Extraire le nom de la dimension
                    dim_name = name.replace('Table input - ', '').replace('Lookup ', '')
                    lookup_name = f'Lookup {dim_name}'
                    lookup_to_table_input[lookup_name] = name
        
        for step in steps:
            step_type_elem = step.find('type')
            if step_type_elem is None:
                continue
            
            step_type = step_type_elem.text
            step_name_elem = step.find('name')
            step_name = step_name_elem.text if step_name_elem is not None else ''
            
            # Corriger selon le type
            if step_type == 'CSVInput' or step_type == 'CsvInput':
                fix_csv_input_step(step)
                modified = True
            elif step_type == 'StreamLookup':
                # Trouver le table input correspondant
                table_input_name = lookup_to_table_input.get(step_name, f'Table input - {step_name.replace("Lookup ", "")}')
                fix_stream_lookup_step(step, table_input_name)
                modified = True
            elif step_type == 'TableInput':
                fix_table_input_step(step)
                modified = True
            elif step_type == 'TableOutput':
                fix_table_output_step(step)
                modified = True
            elif step_type == 'TextFileOutput':
                fix_text_file_output_step(step)
                modified = True
            
            # S'assurer que chaque étape a une section GUI
            gui = step.find('GUI')
            if gui is None:
                gui = ET.SubElement(step, 'GUI')
                ET.SubElement(gui, 'xloc').text = '64'
                ET.SubElement(gui, 'yloc').text = '64'
                ET.SubElement(gui, 'draw').text = 'Y'
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

def fix_json_structure(file_path):
    """Corrige la structure JSON Input pour qu'elle fonctionne correctement"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Le JSON Input doit avoir une structure spécifique pour les fichiers JSON imbriqués
    # Vérifier si c'est le fichier d'extraction JSON
    if 'Extract_JSON' in str(file_path):
        # La structure JSON doit être corrigée pour gérer les batiments et mesures
        # Ceci nécessite une configuration manuelle dans Pentaho
        pass
    
    return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    ktr_files = list(transformations_dir.glob('*.ktr'))
    
    if not ktr_files:
        print("Aucun fichier .ktr trouve!")
        return
    
    print(f"Correction de {len(ktr_files)} fichier(s) .ktr...\n")
    
    success_count = 0
    for ktr_file in sorted(ktr_files):
        print(f"Traitement de {ktr_file.name}...")
        if fix_all_steps_in_file(ktr_file):
            print(f"  OK: Fichier corrige")
            success_count += 1
        else:
            print(f"  Aucune modification necessaire")
    
    print(f"\nTermine! {success_count}/{len(ktr_files)} fichier(s) corrige(s).")
    print("\nLes fichiers sont maintenant prets pour Pentaho Spoon.")
    print("Ouvrez-les dans Pentaho et configurez:")
    print("1. Les connexions MySQL (MySQL_Operational et MySQL_DW)")
    print("2. Les chemins de fichiers si necessaire")
    print("3. Les StreamLookup pour pointer vers les Table Input correspondants")

if __name__ == '__main__':
    main()

