#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation finale de 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'

print(f"=== Validation finale de {ktr_file} ===\n")

tree = ET.parse(ktr_file)

# Verifier CSVInput
csv_step = None
for step in tree.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'CSV file input':
        csv_step = step
        break

if csv_step is not None:
    print("CSVInput:")
    type_elem = csv_step.find('type')
    print(f"  - Type: {type_elem.text if type_elem is not None else 'MANQUANT'}")
    
    number_partitions = csv_step.find('.//partitioning/number_partitions')
    print(f"  - number_partitions: {'OK' if number_partitions is not None else 'MANQUANT'}")
    
    file_elem = csv_step.find('.//file/name')
    print(f"  - File: {file_elem.text if file_elem is not None else 'MANQUANT'}")
    
    fields = [f.find('name').text for f in csv_step.findall('.//field') if f.find('name') is not None]
    print(f"  - Champs: {len(fields)} ({', '.join(fields)})")
    print()

# Verifier Select values
select_step = None
for step in tree.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'Select values':
        select_step = step
        break

if select_step is not None:
    print("Select values:")
    selects = select_step.findall('select')
    print(f"  - Nombre de sections <select>: {len(selects)}")
    
    if len(selects) > 0:
        select_fields = [f.find('name').text for f in selects[0].findall('field') 
                         if f.find('name') is not None]
        print(f"  - Champs dans select: {len(select_fields)} ({', '.join(select_fields)})")
    
    number_partitions = select_step.find('.//partitioning/number_partitions')
    print(f"  - number_partitions: {'OK' if number_partitions is not None else 'MANQUANT'}")
    print()

# Verifier les hops
hops = [(h.find('from').text, h.find('to').text, h.find('enabled').text) 
        for h in tree.findall('.//hop')]
print("Hops:")
for from_step, to_step, enabled in hops:
    status = "OK" if enabled == "Y" else "DESACTIVE"
    print(f"  - {from_step} -> {to_step}: {status}")

all_enabled = all(h[2] == "Y" for h in hops)
print(f"\nTous les hops actives: {'OUI' if all_enabled else 'NON'}")

print("\nValidation terminee!")






