import pickle
import glob
import os
from lxml import etree as ET

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def preprocess_svgs(body_svgs_dir='body_svgs', hair_svgs_dir='hair_svgs'):
    svg_cache = {}

    # Process body SVGs
    body_files = glob.glob(os.path.join(body_svgs_dir, 'Body*.svg'))
    for body_file in body_files:
        tree = ET.parse(body_file)
        root = tree.getroot()

        body_elements = {'tree': ET.tostring(
            root), 'skin': None, 'accessories': []}

        # Inject a comment with the name of the file
        comment = ET.Comment(f'This is a body SVG from file: {
                             os.path.basename(body_file)}')
        root.insert(0, comment)

        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'Head':
                    body_elements['skin'] = elem.attrib['id']
                elif elem.attrib['id'] in ['Tie', 'TieKnot', 'Bowtie']:
                    body_elements['accessories'].append(elem.attrib['id'])

        file_name = os.path.splitext(os.path.basename(body_file))[0]
        svg_cache[file_name] = body_elements

    # Process hair SVGs
    hair_files = glob.glob(os.path.join(hair_svgs_dir, 'Hair*.svg'))
    for hair_file in hair_files:
        tree = ET.parse(hair_file)
        root = tree.getroot()

        hair_elements = {'tree': ET.tostring(
            root), 'hair': None, 'accessory': None}

        # Inject a comment with the name of the file
        comment = ET.Comment(f'This is a hair SVG from file: {
                             os.path.basename(hair_file)}')
        root.insert(0, comment)

        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'hair':
                    hair_elements['hair'] = elem.attrib['id']
                elif elem.attrib['id'] == 'accessory':
                    hair_elements['accessory'] = elem.attrib['id']

        file_name = os.path.splitext(os.path.basename(hair_file))[0]
        svg_cache[file_name] = hair_elements

    # Save the cache to a file
    with open('svg_cache.pkl', 'wb') as cache_file:
        pickle.dump(svg_cache, cache_file)


if __name__ == '__main__':
    preprocess_svgs()
