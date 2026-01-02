"""
Script pour corriger complètement la transformation JSON avec des chemins JSONPath corrects
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def fix_json_input_fields(file_path):
    """Corrige les champs JSON Input pour extraire correctement les données imbriquées"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Trouver l'étape JSON Input
        json_input = None
        for step in root.findall('.//step'):
            step_type = step.find('type')
            if step_type is not None and step_type.text == 'JsonInput':
                json_input = step
                break
        
        if json_input is None:
            return False
        
        # Remplacer les champs existants par des chemins JSONPath corrects
        fields_elem = json_input.find('fields')
        if fields_elem is not None:
            json_input.remove(fields_elem)
        
        fields = ET.SubElement(json_input, 'fields')
        
        # Champ id_region (racine)
        field1 = ET.SubElement(fields, 'field')
        ET.SubElement(field1, 'name').text = 'id_region'
        ET.SubElement(field1, 'path').text = '$.id_region'
        ET.SubElement(field1, 'type').text = 'String'
        ET.SubElement(field1, 'format')
        ET.SubElement(field1, 'currency')
        ET.SubElement(field1, 'decimal')
        ET.SubElement(field1, 'group')
        ET.SubElement(field1, 'length').text = '-1'
        ET.SubElement(field1, 'precision').text = '-1'
        ET.SubElement(field1, 'trim_type').text = 'none'
        ET.SubElement(field1, 'repeat').text = 'N'
        
        # Champ id_batiment (depuis batiments[*])
        field2 = ET.SubElement(fields, 'field')
        ET.SubElement(field2, 'name').text = 'id_batiment'
        ET.SubElement(field2, 'path').text = '$.batiments[*].id_batiment'
        ET.SubElement(field2, 'type').text = 'String'
        ET.SubElement(field2, 'format')
        ET.SubElement(field2, 'currency')
        ET.SubElement(field2, 'decimal')
        ET.SubElement(field2, 'group')
        ET.SubElement(field2, 'length').text = '-1'
        ET.SubElement(field2, 'precision').text = '-1'
        ET.SubElement(field2, 'trim_type').text = 'none'
        ET.SubElement(field2, 'repeat').text = 'Y'
        
        # Champ type_energie
        field3 = ET.SubElement(fields, 'field')
        ET.SubElement(field3, 'name').text = 'type_energie'
        ET.SubElement(field3, 'path').text = '$.batiments[*].type_energie'
        ET.SubElement(field3, 'type').text = 'String'
        ET.SubElement(field3, 'format')
        ET.SubElement(field3, 'currency')
        ET.SubElement(field3, 'decimal')
        ET.SubElement(field3, 'group')
        ET.SubElement(field3, 'length').text = '-1'
        ET.SubElement(field3, 'precision').text = '-1'
        ET.SubElement(field3, 'trim_type').text = 'none'
        ET.SubElement(field3, 'repeat').text = 'Y'
        
        # Champ compteur_id (depuis mesures[*])
        field4 = ET.SubElement(fields, 'field')
        ET.SubElement(field4, 'name').text = 'compteur_id'
        ET.SubElement(field4, 'path').text = '$.batiments[*].mesures[*].compteur_id'
        ET.SubElement(field4, 'type').text = 'String'
        ET.SubElement(field4, 'format')
        ET.SubElement(field4, 'currency')
        ET.SubElement(field4, 'decimal')
        ET.SubElement(field4, 'group')
        ET.SubElement(field4, 'length').text = '-1'
        ET.SubElement(field4, 'precision').text = '-1'
        ET.SubElement(field4, 'trim_type').text = 'none'
        ET.SubElement(field4, 'repeat').text = 'Y'
        
        # Champ date_mesure
        field5 = ET.SubElement(fields, 'field')
        ET.SubElement(field5, 'name').text = 'date_mesure'
        ET.SubElement(field5, 'path').text = '$.batiments[*].mesures[*].date_mesure'
        ET.SubElement(field5, 'type').text = 'String'
        ET.SubElement(field5, 'format')
        ET.SubElement(field5, 'currency')
        ET.SubElement(field5, 'decimal')
        ET.SubElement(field5, 'group')
        ET.SubElement(field5, 'length').text = '-1'
        ET.SubElement(field5, 'precision').text = '-1'
        ET.SubElement(field5, 'trim_type').text = 'none'
        ET.SubElement(field5, 'repeat').text = 'Y'
        
        # Champ consommation_kWh
        field6 = ET.SubElement(fields, 'field')
        ET.SubElement(field6, 'name').text = 'consommation_kWh'
        ET.SubElement(field6, 'path').text = '$.batiments[*].mesures[*].consommation_kWh'
        ET.SubElement(field6, 'type').text = 'Number'
        ET.SubElement(field6, 'format')
        ET.SubElement(field6, 'currency')
        ET.SubElement(field6, 'decimal')
        ET.SubElement(field6, 'group')
        ET.SubElement(field6, 'length').text = '-1'
        ET.SubElement(field6, 'precision').text = '-1'
        ET.SubElement(field6, 'trim_type').text = 'none'
        ET.SubElement(field6, 'repeat').text = 'Y'
        
        # Champ consommation_m3
        field7 = ET.SubElement(fields, 'field')
        ET.SubElement(field7, 'name').text = 'consommation_m3'
        ET.SubElement(field7, 'path').text = '$.batiments[*].mesures[*].consommation_m3'
        ET.SubElement(field7, 'type').text = 'Number'
        ET.SubElement(field7, 'format')
        ET.SubElement(field7, 'currency')
        ET.SubElement(field7, 'decimal')
        ET.SubElement(field7, 'group')
        ET.SubElement(field7, 'length').text = '-1'
        ET.SubElement(field7, 'precision').text = '-1'
        ET.SubElement(field7, 'trim_type').text = 'none'
        ET.SubElement(field7, 'repeat').text = 'Y'
        
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        return True
        
    except Exception as e:
        print(f"  ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    json_file = transformations_dir / '01_Extract_JSON_Consumption.ktr'
    
    if json_file.exists():
        print("Correction de la transformation JSON...")
        if fix_json_input_fields(json_file):
            print("  OK: Transformation JSON corrigee")
            print("\nNOTE: La transformation utilise maintenant des chemins JSONPath")
            print("      pour extraire directement les mesures depuis les batiments.")
            print("      Vous devrez peut-etre ajuster les chemins dans Pentaho Spoon")
            print("      selon la structure exacte de vos fichiers JSON.")
        else:
            print("  Aucune modification necessaire")
    else:
        print("Fichier non trouve: 01_Extract_JSON_Consumption.ktr")

if __name__ == '__main__':
    main()

