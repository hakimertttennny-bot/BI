"""
Script pour créer une transformation JSON correcte avec JSON Input Fields
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def create_json_input_fields_step():
    """Crée une étape JSON Input Fields pour extraire les données imbriquées"""
    step = ET.Element('step')
    
    ET.SubElement(step, 'name').text = 'JSON Input Fields'
    ET.SubElement(step, 'type').text = 'JsonInputFields'
    ET.SubElement(step, 'description').text = 'Extraction des données depuis les fichiers JSON imbriqués'
    ET.SubElement(step, 'distribute').text = 'Y'
    ET.SubElement(step, 'custom_distribution')
    ET.SubElement(step, 'copies').text = '1'
    
    partitioning = ET.SubElement(step, 'partitioning')
    ET.SubElement(partitioning, 'method').text = 'none'
    ET.SubElement(partitioning, 'schema_name')
    ET.SubElement(partitioning, 'number_partitions')
    
    file_elem = ET.SubElement(step, 'file')
    ET.SubElement(file_elem, 'name').text = '${Internal.Transformation.Filename.Directory}/data/source/${TYPE_ENERGIE}_consumption_${MOIS}_${ANNEE}.json'
    ET.SubElement(file_elem, 'filemask')
    ET.SubElement(file_elem, 'exclude_filemask')
    ET.SubElement(file_elem, 'file_required').text = 'N'
    ET.SubElement(file_elem, 'include_subfolders').text = 'N'
    
    # Configuration pour extraire les données imbriquées
    # Utiliser des chemins JSONPath pour extraire directement les mesures
    fields = ET.SubElement(step, 'fields')
    
    # Champ pour id_region (depuis la racine)
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
    
    # Champ pour id_batiment (depuis batiments[*])
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
    
    # Champ pour type_energie
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
    
    # Champ pour compteur_id (depuis mesures[*])
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
    
    # Champ pour date_mesure
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
    
    # Champ pour consommation_kWh
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
    
    # Champ pour consommation_m3
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
    
    ET.SubElement(step, 'removeSourceField').text = 'N'
    ET.SubElement(step, 'IsIgnoreEmptyFile').text = 'false'
    ET.SubElement(step, 'doNotFailIfNoFile').text = 'false'
    ET.SubElement(step, 'ignoreMissingPath').text = 'false'
    ET.SubElement(step, 'defaultPathLeaf').text = 'null'
    ET.SubElement(step, 'readUrl').text = 'N'
    ET.SubElement(step, 'ignoreEmptyFile').text = 'false'
    ET.SubElement(step, 'RowLimit').text = '0'
    
    gui = ET.SubElement(step, 'GUI')
    ET.SubElement(gui, 'xloc').text = '64'
    ET.SubElement(gui, 'yloc').text = '64'
    ET.SubElement(gui, 'draw').text = 'Y'
    
    return step

# En fait, dans Pentaho, il vaut mieux utiliser une approche avec plusieurs étapes
# ou utiliser JSON Input avec des chemins corrects. Laissez-moi créer une version simplifiée
# qui sera plus facile à configurer dans Pentaho Spoon.

