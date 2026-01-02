#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige definitivement 09_Load_Environmental_DM.ktr"""

import xml.etree.ElementTree as ET
import re

def main():
    ktr_file = 'pentaho/transformations/09_Load_Environmental_DM.ktr'
    
    print(f"Lecture de {ktr_file}...")
    with open(ktr_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corriger Lookup Batiment
    pattern_batiment = r'(<step>\s*<name>Lookup Batiment</name>.*?<partitioning>.*?</partitioning>)\s*(<from/>.*?</integer_pair>)\s*(<lookup>.*?</lookup>)'
    replacement_batiment = r'''\1
    <lookup>
      <step>Table input - Lookup Batiment</step>
      <keys>
        <key>
          <name>id_batiment</name>
          <field>id_batiment</field>
          <name2>id_batiment</name2>
        </key>
      </keys>
      <value>
        <name>id_batiment_sk</name>
      </value>
    </lookup>
    <memory_preserve>N</memory_preserve>
    <sorted_list>N</sorted_list>
    <integer_pair>N</integer_pair>'''
    
    content = re.sub(pattern_batiment, replacement_batiment, content, flags=re.DOTALL)
    
    # Corriger Lookup Region
    pattern_region = r'(<step>\s*<name>Lookup Region</name>.*?<partitioning>.*?</partitioning>)\s*(<from/>.*?</integer_pair>)\s*(<lookup>.*?</lookup>)'
    replacement_region = r'''\1
    <lookup>
      <step>Table input - Lookup Region</step>
      <keys>
        <key>
          <name>id_region</name>
          <field>id_region</field>
          <name2>id_region</name2>
        </key>
      </keys>
      <value>
        <name>id_region_sk</name>
      </value>
    </lookup>
    <memory_preserve>N</memory_preserve>
    <sorted_list>N</sorted_list>
    <integer_pair>N</integer_pair>'''
    
    content = re.sub(pattern_region, replacement_region, content, flags=re.DOTALL)
    
    # Corriger Lookup Temps
    pattern_temps = r'(<step>\s*<name>Lookup Temps</name>.*?<partitioning>.*?</partitioning>)\s*(<from/>.*?</integer_pair>)\s*(<lookup>.*?</lookup>)'
    replacement_temps = r'''\1
    <lookup>
      <step>Table input - Lookup Temps</step>
      <keys>
        <key>
          <name>date_rapport</name>
          <field>date_rapport</field>
          <name2>date_complete</name2>
        </key>
      </keys>
      <value>
        <name>id_temps_sk</name>
      </value>
    </lookup>
    <memory_preserve>N</memory_preserve>
    <sorted_list>N</sorted_list>
    <integer_pair>N</integer_pair>'''
    
    content = re.sub(pattern_temps, replacement_temps, content, flags=re.DOTALL)
    
    # Corriger CSVInput - remplacer completement
    pattern_csv = r'<step>\s*<name>CSV file input</name>.*?</step>'
    replacement_csv = '''<step>
    <name>CSV file input</name>
    <type>CSVInput</type>
    <description>Lecture des donnees transformees</description>
    <distribute>Y</distribute>
    <custom_distribution/>
    <copies>1</copies>
    <partitioning>
      <method>none</method>
      <schema_name/>
      <number_partitions/>
    </partitioning>
    <file>
      <name>${Internal.Transformation.Filename.Directory}/data/transformed/environmental_transformed.csv</name>
      <filemask/>
      <exclude_filemask/>
      <file_required>N</file_required>
      <include_subfolders>N</include_subfolders>
    </file>
    <field>
      <name>id_region</name>
      <type>String</type>
      <format/>
      <currency/>
      <decimal/>
      <group/>
      <trim_type>both</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <field>
      <name>id_batiment</name>
      <type>String</type>
      <format/>
      <currency/>
      <decimal/>
      <group/>
      <trim_type>both</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <field>
      <name>date_rapport</name>
      <type>String</type>
      <format/>
      <currency/>
      <decimal/>
      <group/>
      <trim_type>both</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <field>
      <name>emission_CO2_kg</name>
      <type>Number</type>
      <format/>
      <currency/>
      <decimal>.</decimal>
      <group/>
      <trim_type>none</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <field>
      <name>taux_recyclage</name>
      <type>Number</type>
      <format/>
      <currency/>
      <decimal>.</decimal>
      <group/>
      <trim_type>none</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <field>
      <name>ratio_CO2_consommation</name>
      <type>Number</type>
      <format/>
      <currency/>
      <decimal>.</decimal>
      <group/>
      <trim_type>none</trim_type>
      <length>-1</length>
      <precision>-1</precision>
    </field>
    <separator>;</separator>
    <enclosure>"</enclosure>
    <escape/>
    <header>true</header>
    <footer>false</footer>
    <wiped>false</wiped>
    <lazyConversion>false</lazyConversion>
    <attributes/>
    <cluster_schema/>
    <remotesteps>
      <input>
      </input>
      <output>
      </output>
    </remotesteps>
    <GUI>
      <xloc>416</xloc>
      <yloc>384</yloc>
      <draw>Y</draw>
    </GUI>
  </step>'''
    
    content = re.sub(pattern_csv, replacement_csv, content, flags=re.DOTALL)
    
    # Activer les hops
    content = content.replace('<from>CSV file input</from>\n      <to>Lookup Region</to>\n      <enabled>N</enabled>', 
                              '<from>CSV file input</from>\n      <to>Lookup Region</to>\n      <enabled>Y</enabled>')
    content = content.replace('<from>Table input - Lookup Region</from>\n      <to>Lookup Region</to>\n      <enabled>N</enabled>',
                              '<from>Table input - Lookup Region</from>\n      <to>Lookup Region</to>\n      <enabled>Y</enabled>')
    content = content.replace('<from>Table input - Lookup Batiment</from>\n      <to>Lookup Batiment</to>\n      <enabled>N</enabled>',
                              '<from>Table input - Lookup Batiment</from>\n      <to>Lookup Batiment</to>\n      <enabled>Y</enabled>')
    content = content.replace('<from>Table input - Lookup Temps</from>\n      <to>Lookup Temps</to>\n      <enabled>N</enabled>',
                              '<from>Table input - Lookup Temps</from>\n      <to>Lookup Temps</to>\n      <enabled>Y</enabled>')
    content = content.replace('<from>Lookup Batiment</from>\n      <to>Lookup Temps</to>\n      <enabled>N</enabled>',
                              '<from>Lookup Batiment</from>\n      <to>Lookup Temps</to>\n      <enabled>Y</enabled>')
    content = content.replace('<from>Lookup Temps</from>\n      <to>Table output</to>\n      <enabled>N</enabled>',
                              '<from>Lookup Temps</from>\n      <to>Table output</to>\n      <enabled>Y</enabled>')
    
    # Ajouter schema aux Table Input
    content = content.replace('<connection>MySQL_DW</connection>\n    <sql>SELECT * FROM Dim_Region_Environnement </sql>',
                              '<connection>MySQL_DW</connection>\n    <schema/>\n    <sql>SELECT * FROM Dim_Region_Environnement </sql>')
    content = content.replace('<connection>MySQL_DW</connection>\n    <sql>SELECT * FROM Dim_Batiment_Environnement </sql>',
                              '<connection>MySQL_DW</connection>\n    <schema/>\n    <sql>SELECT * FROM Dim_Batiment_Environnement </sql>')
    content = content.replace('<connection>MySQL_DW</connection>\n    <sql>SELECT * FROM Dim_Temps </sql>',
                              '<connection>MySQL_DW</connection>\n    <schema/>\n    <sql>SELECT * FROM Dim_Temps </sql>')
    
    # Sauvegarder
    print(f"Ecriture de {ktr_file}...")
    with open(ktr_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK: Fichier corrige avec succes!")

if __name__ == '__main__':
    main()






