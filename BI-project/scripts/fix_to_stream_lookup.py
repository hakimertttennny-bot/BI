"""
Script pour remplacer DatabaseValueLookup par StreamLookup avec Table Input
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def create_table_input_step(step_name, table_name, connection_name, xloc, yloc):
    """Crée une étape Table Input pour charger une dimension"""
    step = ET.Element('step')
    
    name_elem = ET.SubElement(step, 'name')
    name_elem.text = f'Table input - {step_name}'
    
    type_elem = ET.SubElement(step, 'type')
    type_elem.text = 'TableInput'
    
    description_elem = ET.SubElement(step, 'description')
    description_elem.text = f'Chargement de la dimension {step_name}'
    
    ET.SubElement(step, 'distribute').text = 'Y'
    ET.SubElement(step, 'custom_distribution')
    ET.SubElement(step, 'copies').text = '1'
    
    partitioning = ET.SubElement(step, 'partitioning')
    ET.SubElement(partitioning, 'method').text = 'none'
    ET.SubElement(partitioning, 'schema_name')
    ET.SubElement(partitioning, 'number_partitions')
    
    ET.SubElement(step, 'connection').text = connection_name
    ET.SubElement(step, 'schema')
    
    sql_elem = ET.SubElement(step, 'sql')
    sql_elem.text = f'SELECT * FROM {table_name} WHERE est_actif = TRUE'
    
    ET.SubElement(step, 'execute_each_row').text = 'false'
    ET.SubElement(step, 'variables_active').text = 'false'
    ET.SubElement(step, 'lazy_conversion_active').text = 'false'
    
    gui = ET.SubElement(step, 'GUI')
    ET.SubElement(gui, 'xloc').text = str(xloc)
    ET.SubElement(gui, 'yloc').text = str(yloc - 100)  # Au-dessus du StreamLookup
    ET.SubElement(gui, 'draw').text = 'Y'
    
    return step

def create_stream_lookup_step(old_lookup_step, lookup_name, xloc, yloc):
    """Convertit une étape DatabaseValueLookup en StreamLookup"""
    # Créer une nouvelle étape StreamLookup
    step = ET.Element('step')
    
    name_elem = ET.SubElement(step, 'name')
    name_elem.text = f'Stream Lookup - {lookup_name}'
    
    type_elem = ET.SubElement(step, 'type')
    type_elem.text = 'StreamLookup'
    
    description_elem = ET.SubElement(step, 'description')
    description_elem.text = f'Lookup de la dimension {lookup_name}'
    
    ET.SubElement(step, 'distribute').text = 'Y'
    ET.SubElement(step, 'custom_distribution')
    ET.SubElement(step, 'copies').text = '1'
    
    partitioning = ET.SubElement(step, 'partitioning')
    ET.SubElement(partitioning, 'method').text = 'none'
    ET.SubElement(partitioning, 'schema_name')
    ET.SubElement(partitioning, 'number_partitions')
    
    # Récupérer les clés et valeurs de l'ancienne étape
    keys = old_lookup_step.findall('.//key')
    values = old_lookup_step.findall('.//value')
    
    # Configuration StreamLookup
    lookup = ET.SubElement(step, 'lookup')
    ET.SubElement(lookup, 'step').text = f'Table input - {lookup_name}'
    
    # Ajouter les clés
    key_field = ET.SubElement(lookup, 'key')
    if keys:
        key = keys[0]
        ET.SubElement(key_field, 'name').text = key.find('field').text if key.find('field') is not None else ''
        ET.SubElement(key_field, 'field').text = key.find('field').text if key.find('field') is not None else ''
    
    # Ajouter les valeurs
    value_field = ET.SubElement(lookup, 'value')
    if values:
        for val in values:
            val_elem = ET.SubElement(value_field, 'name')
            val_elem.text = val.find('rename').text if val.find('rename') is not None else val.find('name').text
    
    ET.SubElement(step, 'memory_preserve').text = 'N'
    ET.SubElement(step, 'order_lookup').text = 'N'
    
    gui = ET.SubElement(step, 'GUI')
    ET.SubElement(gui, 'xloc').text = str(xloc)
    ET.SubElement(gui, 'yloc').text = str(yloc)
    ET.SubElement(gui, 'draw').text = 'Y'
    
    return step

def fix_transformation_file(file_path, lookups_config):
    """Corrige un fichier de transformation"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Trouver toutes les étapes DatabaseValueLookup
        steps = root.findall('.//step')
        lookup_steps = [s for s in steps if s.find('type') is not None and s.find('type').text == 'DatabaseValueLookup']
        
        if not lookup_steps:
            return False
        
        # Récupérer l'ordre des hops
        order_elem = root.find('order')
        
        modified = False
        xloc_offset = 0
        
        for lookup_step in lookup_steps:
            lookup_name = lookup_step.find('name').text.replace('Lookup ', '')
            table_elem = lookup_step.find('table')
            connection_elem = lookup_step.find('connection')
            
            if table_elem is None or connection_elem is None:
                continue
            
            table_name = table_elem.text
            connection_name = connection_elem.text
            
            # Coordonnées
            gui = lookup_step.find('GUI')
            if gui is not None:
                xloc = int(gui.find('xloc').text) if gui.find('xloc') is not None else 192
                yloc = int(gui.find('yloc').text) if gui.find('yloc') is not None else 64
            else:
                xloc = 192
                yloc = 64
            
            # Créer Table Input
            table_input = create_table_input_step(lookup_name, table_name, connection_name, xloc, yloc)
            
            # Créer Stream Lookup
            stream_lookup = create_stream_lookup_step(lookup_step, lookup_name, xloc, yloc)
            
            # Remplacer l'ancienne étape
            parent = root.find('.//step[type="DatabaseValueLookup"]/..')
            if parent is None:
                steps_elem = root.find('steps') if root.find('steps') is not None else root
                steps_elem.insert(list(steps_elem).index(lookup_step), table_input)
                steps_elem.insert(list(steps_elem).index(lookup_step) + 1, stream_lookup)
                steps_elem.remove(lookup_step)
            else:
                parent.insert(list(parent).index(lookup_step), table_input)
                parent.insert(list(parent).index(lookup_step) + 1, stream_lookup)
                parent.remove(lookup_step)
            
            # Mettre à jour les hops
            old_name = lookup_step.find('name').text
            new_table_name = table_input.find('name').text
            new_lookup_name = stream_lookup.find('name').text
            
            for hop in order_elem.findall('hop'):
                if hop.find('from') is not None and hop.find('from').text == old_name:
                    hop.find('from').text = new_lookup_name
                if hop.find('to') is not None and hop.find('to').text == old_name:
                    hop.find('to').text = new_table_name
                    # Ajouter un hop de Table Input vers Stream Lookup
                    new_hop = ET.Element('hop')
                    ET.SubElement(new_hop, 'from').text = new_table_name
                    ET.SubElement(new_hop, 'to').text = new_lookup_name
                    ET.SubElement(new_hop, 'enabled').text = 'true'
                    order_elem.append(new_hop)
            
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

# Approche plus simple : remplacer juste le type
def simple_fix(file_path):
    """Remplace simplement DatabaseValueLookup par StreamLookup"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer le type
    new_content = content.replace('<type>DatabaseValueLookup</type>', '<type>StreamLookup</type>')
    
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
    
    print("Remplacement de DatabaseValueLookup par StreamLookup...")
    print("NOTE: Vous devrez configurer manuellement les StreamLookup dans Pentaho")
    print("      pour pointer vers les Table Input qui chargent les dimensions.\n")
    
    for filename in files_to_fix:
        file_path = transformations_dir / filename
        if file_path.exists():
            print(f"Traitement de {filename}...")
            if simple_fix(file_path):
                print(f"  OK: Type remplace par StreamLookup")
                print(f"  ATTENTION: Vous devrez reconfigurer les etapes dans Pentaho Spoon")
            else:
                print(f"  Aucune modification necessaire")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")
    print("\nPROCHAINES ETAPES:")
    print("1. Ouvrir les transformations dans Pentaho Spoon")
    print("2. Pour chaque StreamLookup:")
    print("   - Ajouter une etape 'Table Input' avant le StreamLookup")
    print("   - Configurer le Table Input pour charger la dimension depuis MySQL_DW")
    print("   - Configurer le StreamLookup pour utiliser le Table Input comme source")

if __name__ == '__main__':
    main()

