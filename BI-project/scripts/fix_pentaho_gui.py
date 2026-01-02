"""
Script pour ajouter les sections GUI manquantes dans les fichiers .ktr Pentaho
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

def add_gui_to_step(step_elem, xloc, yloc):
    """Ajoute une section GUI à une étape si elle n'existe pas"""
    # Vérifier si GUI existe déjà
    gui = step_elem.find('GUI')
    if gui is None:
        gui = ET.SubElement(step_elem, 'GUI')
        ET.SubElement(gui, 'xloc').text = str(xloc)
        ET.SubElement(gui, 'yloc').text = str(yloc)
        ET.SubElement(gui, 'draw').text = 'Y'
    else:
        # Mettre à jour les coordonnées si elles existent
        xloc_elem = gui.find('xloc')
        yloc_elem = gui.find('yloc')
        if xloc_elem is not None:
            xloc_elem.text = str(xloc)
        else:
            ET.SubElement(gui, 'xloc').text = str(xloc)
        if yloc_elem is not None:
            yloc_elem.text = str(yloc)
        else:
            ET.SubElement(gui, 'yloc').text = str(yloc)
        draw_elem = gui.find('draw')
        if draw_elem is None:
            ET.SubElement(gui, 'draw').text = 'Y'

def fix_ktr_file(file_path):
    """Corrige un fichier .ktr en ajoutant les sections GUI"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Trouver toutes les étapes
        steps = root.findall('.//step')
        
        if not steps:
            print(f"  Aucune étape trouvée dans {file_path}")
            return False
        
        # Coordonnées initiales
        xloc = 64
        yloc = 64
        x_offset = 128  # Espacement horizontal entre les étapes
        
        # Ajouter GUI à chaque étape
        for i, step in enumerate(steps):
            step_name = step.find('name')
            if step_name is not None:
                add_gui_to_step(step, xloc, yloc)
                xloc += x_offset
        
        # Sauvegarder le fichier
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        print(f"  OK: {len(steps)} etapes corrigees")
        return True
        
    except Exception as e:
        print(f"  ERREUR: {e}")
        return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent.parent
    transformations_dir = project_root / 'pentaho' / 'transformations'
    
    if not transformations_dir.exists():
        print(f"Le répertoire {transformations_dir} n'existe pas!")
        return
    
    ktr_files = list(transformations_dir.glob('*.ktr'))
    
    if not ktr_files:
        print("Aucun fichier .ktr trouvé!")
        return
    
    print(f"Correction de {len(ktr_files)} fichier(s) .ktr...\n")
    
    success_count = 0
    for ktr_file in sorted(ktr_files):
        print(f"Traitement de {ktr_file.name}...")
        if fix_ktr_file(ktr_file):
            success_count += 1
        print()
    
    print(f"Terminé! {success_count}/{len(ktr_files)} fichier(s) corrigé(s).")

if __name__ == '__main__':
    main()

