"""
Script complet pour remplacer DatabaseValueLookup par StreamLookup avec Table Input
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def add_table_input_before_lookup(root, lookup_step, table_name, connection_name):
    """Ajoute une étape Table Input avant un StreamLookup"""
    # Créer l'étape Table Input
    table_input = ET.Element('step')
    
    ET.SubElement(table_input, 'name').text = f'Table input - {lookup_step.find("name").text.replace("Stream Lookup - ", "")}'
    ET.SubElement(table_input, 'type').text = 'TableInput'
    ET.SubElement(table_input, 'description').text = f'Chargement de la dimension depuis {table_name}'
    ET.SubElement(table_input, 'distribute').text = 'Y'
    ET.SubElement(table_input, 'custom_distribution')
    ET.SubElement(table_input, 'copies').text = '1'
    
    partitioning = ET.SubElement(table_input, 'partitioning')
    ET.SubElement(partitioning, 'method').text = 'none'
    ET.SubElement(partitioning, 'schema_name')
    ET.SubElement(partitioning, 'number_partitions')
    
    ET.SubElement(table_input, 'connection').text = connection_name
    ET.SubElement(table_input, 'schema')
    
    sql_elem = ET.SubElement(table_input, 'sql')
    sql_elem.text = f'SELECT * FROM {table_name} WHERE est_actif = TRUE'
    
    ET.SubElement(table_input, 'execute_each_row').text = 'false'
    ET.SubElement(table_input, 'variables_active').text = 'false'
    ET.SubElement(table_input, 'lazy_conversion_active').text = 'false'
    
    # Positionner au-dessus du StreamLookup
    lookup_gui = lookup_step.find('GUI')
    if lookup_gui is not None:
        xloc = int(lookup_gui.find('xloc').text) if lookup_gui.find('xloc') is not None else 192
        yloc = int(lookup_gui.find('yloc').text) if lookup_gui.find('yloc') is not None else 64
    else:
        xloc = 192
        yloc = 64
    
    gui = ET.SubElement(table_input, 'GUI')
    ET.SubElement(gui, 'xloc').text = str(xloc)
    ET.SubElement(gui, 'yloc').text = str(yloc - 100)
    ET.SubElement(gui, 'draw').text = 'Y'
    
    return table_input

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
        
        # Mapping des noms de lookup vers les tables
        lookup_to_table = {}
        lookup_to_connection = {}
        
        # Pour chaque StreamLookup, déterminer la table et la connexion
        for lookup in stream_lookups:
            lookup_name = lookup.find('name').text
            # Extraire le nom de la dimension du nom de l'étape
            if 'Region' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Region_Consommation' if 'Consumption' in str(file_path) else ('Dim_Region_Rentabilite' if 'Rentabilite' in str(file_path) else 'Dim_Region_Environnement')
            elif 'Batiment' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Batiment_Consommation' if 'Consumption' in str(file_path) else ('Dim_Batiment_Rentabilite' if 'Rentabilite' in str(file_path) else 'Dim_Batiment_Environnement')
            elif 'Client' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Client_Consommation' if 'Consumption' in str(file_path) else 'Dim_Client_Rentabilite'
            elif 'Compteur' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Compteur'
            elif 'Type Energie' in lookup_name or 'Type_Energie' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Type_Energie'
            elif 'Temps' in lookup_name:
                lookup_to_table[lookup_name] = 'Dim_Temps'
            
            lookup_to_connection[lookup_name] = 'MySQL_DW'
        
        modified = False
        steps_elem = root.find('.//step[1]/..') if root.find('.//step') is not None else root
        
        for lookup in stream_lookups:
            lookup_name = lookup.find('name').text
            table_name = lookup_to_table.get(lookup_name)
            connection_name = lookup_to_connection.get(lookup_name, 'MySQL_DW')
            
            if not table_name:
                continue
            
            # Vérifier si un Table Input existe déjà
            table_input_name = f'Table input - {lookup_name.replace("Stream Lookup - ", "")}'
            existing_table_input = None
            for step in steps:
                if step.find('name') is not None and step.find('name').text == table_input_name:
                    existing_table_input = step
                    break
            
            if existing_table_input is None:
                # Créer et ajouter le Table Input
                table_input = add_table_input_before_lookup(root, lookup, table_name, connection_name)
                
                # Insérer avant le StreamLookup
                if steps_elem is not None:
                    lookup_index = list(steps_elem).index(lookup) if lookup in list(steps_elem) else len(list(steps_elem))
                    steps_elem.insert(lookup_index, table_input)
                    modified = True
                
                # Mettre à jour les hops
                order_elem = root.find('order')
                if order_elem is not None:
                    # Trouver le hop qui pointe vers le StreamLookup
                    for hop in order_elem.findall('hop'):
                        if hop.find('to') is not None and hop.find('to').text == lookup_name:
                            # Créer un nouveau hop de Table Input vers StreamLookup
                            new_hop = ET.Element('hop')
                            ET.SubElement(new_hop, 'from').text = table_input.find('name').text
                            ET.SubElement(new_hop, 'to').text = lookup_name
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

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    files_to_fix = [
        '05_Load_Consumption_DM.ktr',
        '08_Load_Rentabilite_DM.ktr',
        '09_Load_Environmental_DM.ktr'
    ]
    
    print("Ajout des Table Input pour les StreamLookup...\n")
    
    for filename in files_to_fix:
        file_path = transformations_dir / filename
        if file_path.exists():
            print(f"Traitement de {filename}...")
            if fix_file(file_path):
                print(f"  OK: Table Input ajoutes")
            else:
                print(f"  Aucune modification necessaire")
        else:
            print(f"  Fichier non trouve: {filename}")
    
    print("\nTermine!")
    print("\nLes transformations utilisent maintenant StreamLookup avec Table Input.")
    print("Ouvrez-les dans Pentaho Spoon et configurez les StreamLookup pour")
    print("utiliser les Table Input correspondants comme source de lookup.")

if __name__ == '__main__':
    main()

