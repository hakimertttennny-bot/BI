#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valide 02_Extract_CSV_Environmental.ktr"""

import xml.etree.ElementTree as ET

ktr_file = 'pentaho/transformations/02_Extract_CSV_Environmental.ktr'

print(f"=== Validation de {ktr_file} ===\n")

tree = ET.parse(ktr_file)
root = tree.getroot()

# Verifier CSVInput
csv_step = None
for step in root.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'CSV file input':
        csv_step = step
        break

if csv_step is not None:
    print("CSVInput:")
    type_elem = csv_step.find('type')
    print(f"  - Type: {type_elem.text if type_elem is not None else 'MANQUANT'}")
    
    file_elem = csv_step.find('.//file/name')
    print(f"  - File: {file_elem.text if file_elem is not None else 'MANQUANT'}")
    
    fields = [f.find('name').text for f in csv_step.findall('.//field') if f.find('name') is not None]
    print(f"  - Champs: {len(fields)} ({', '.join(fields)})")
    
    header = csv_step.find('header')
    print(f"  - Header: {header.text if header is not None else 'MANQUANT'}")
    print()

# Verifier les hops
hops = [(h.find('from').text, h.find('to').text, h.find('enabled').text) 
        for h in root.findall('.//hop')]
print("Hops:")
for from_step, to_step, enabled in hops:
    status = "OK" if enabled == "Y" else "DESACTIVE"
    print(f"  - {from_step} -> {to_step}: {status}")

all_enabled = all(h[2] == "Y" for h in hops)
print(f"\nTous les hops actives: {'OUI' if all_enabled else 'NON'}")

# Verifier Select values
select_step = None
for step in root.findall('.//step'):
    name_elem = step.find('name')
    if name_elem is not None and name_elem.text == 'Select values':
        select_step = step
        break

if select_step is not None:
    select_fields = [f.find('name').text for f in select_step.findall('.//select/field') 
                     if f.find('name') is not None]
    print(f"\nSelect values: {len(select_fields)} champs ({', '.join(select_fields)})")

print("\nValidation terminee!")






