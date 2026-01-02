#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige le CSVInput dans 09_Load_Environmental_DM.ktr"""

import xml.etree.ElementTree as ET

def main():
    ktr_file = 'pentaho/transformations/09_Load_Environmental_DM.ktr'
    
    tree = ET.parse(ktr_file)
    root = tree.getroot()
    
    # Trouver CSVInput
    for step in root.findall('.//step'):
        name_elem = step.find('name')
        if name_elem is not None and name_elem.text == 'CSV file input':
            # Changer type
            type_elem = step.find('type')
            if type_elem is not None:
                type_elem.text = 'CSVInput'
            
            # Supprimer anciens elements
            for tag in ['filename', 'filename_field', 'rownum_field', 'include_filename',
                        'separator', 'enclosure', 'header', 'buffer_size', 'lazy_conversion',
                        'add_filename_result', 'parallel', 'newline_possible', 'format', 'encoding', 'fields']:
                for elem in step.findall(tag):
                    step.remove(elem)
            
            # Ajouter file element
            file_elem = ET.SubElement(step, 'file')
            name_elem = ET.SubElement(file_elem, 'name')
            name_elem.text = '${Internal.Transformation.Filename.Directory}/data/transformed/environmental_transformed.csv'
            ET.SubElement(file_elem, 'filemask')
            ET.SubElement(file_elem, 'exclude_filemask')
            file_required = ET.SubElement(file_elem, 'file_required')
            file_required.text = 'N'
            include_subfolders = ET.SubElement(file_elem, 'include_subfolders')
            include_subfolders.text = 'N'
            
            # Ajouter fields
            fields_data = [
                ('id_region', 'String'),
                ('id_batiment', 'String'),
                ('date_rapport', 'String'),
                ('emission_CO2_kg', 'Number'),
                ('taux_recyclage', 'Number'),
                ('ratio_CO2_consommation', 'Number')
            ]
            
            for field_name, field_type in fields_data:
                field_elem = ET.SubElement(step, 'field')
                name_elem = ET.SubElement(field_elem, 'name')
                name_elem.text = field_name
                type_elem = ET.SubElement(field_elem, 'type')
                type_elem.text = field_type
                ET.SubElement(field_elem, 'format')
                ET.SubElement(field_elem, 'currency')
                decimal_elem = ET.SubElement(field_elem, 'decimal')
                if field_type == 'Number':
                    decimal_elem.text = '.'
                ET.SubElement(field_elem, 'group')
                trim_type = ET.SubElement(field_elem, 'trim_type')
                trim_type.text = 'both' if field_type == 'String' else 'none'
                length = ET.SubElement(field_elem, 'length')
                length.text = '-1'
                precision = ET.SubElement(field_elem, 'precision')
                precision.text = '-1'
            
            # Ajouter parametres CSV
            separator = ET.SubElement(step, 'separator')
            separator.text = ';'
            enclosure = ET.SubElement(step, 'enclosure')
            enclosure.text = '"'
            ET.SubElement(step, 'escape')
            header = ET.SubElement(step, 'header')
            header.text = 'true'
            footer = ET.SubElement(step, 'footer')
            footer.text = 'false'
            wiped = ET.SubElement(step, 'wiped')
            wiped.text = 'false'
            lazyConversion = ET.SubElement(step, 'lazyConversion')
            lazyConversion.text = 'false'
            
            break
    
    # Sauvegarder
    tree.write(ktr_file, encoding='utf-8', xml_declaration=True)
    print("OK: CSVInput corrige!")

if __name__ == '__main__':
    main()






