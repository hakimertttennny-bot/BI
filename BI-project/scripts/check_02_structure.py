import xml.etree.ElementTree as ET

tree = ET.parse('pentaho/transformations/02_Extract_CSV_Environmental.ktr')
root = tree.getroot()

# Find CSV input step
for step in root.findall('.//step'):
    if step.find('name') is not None and step.find('name').text == 'CSV file input':
        print("Found CSV file input step")
        file_elem = step.find('file')
        if file_elem is not None:
            name_elem = file_elem.find('name')
            if name_elem is not None:
                print(f"File name: {name_elem.text}")
            else:
                print("ERROR: <name> element not found in <file>")
        else:
            print("ERROR: <file> element not found")
        break

# Find Select values step
for step in root.findall('.//step'):
    if step.find('name') is not None and step.find('name').text == 'Select values':
        print("\nFound Select values step")
        select_elem = step.find('select')
        if select_elem is not None:
            fields = select_elem.findall('field')
            print(f"Number of fields in <select>: {len(fields)}")
            for field in fields:
                name_elem = field.find('name')
                if name_elem is not None:
                    print(f"  - {name_elem.text}")
        else:
            print("ERROR: <select> element not found")
        break





