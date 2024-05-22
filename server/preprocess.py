import pickle
import xml.etree.ElementTree as ET
import glob
import os

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def preprocess_svgs(body_svgs_dir='body_svgs', hair_svgs_dir='hair_svgs'):
    svg_cache = {}

    # Debug: Print current working directory
    print("Current working directory:", os.getcwd())

    # Process body SVGs
    body_files = glob.glob(os.path.join(body_svgs_dir, 'Body*.svg'))
    # Debug: Print the list of body files found
    print("Body files found:", body_files)

    for body_file in body_files:
        tree = ET.parse(body_file)
        root = tree.getroot()
        
        body_elements = {'tree': tree, 'skin': None, 'accessory': None}
        
        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'skin':
                    body_elements['skin'] = elem
                elif elem.attrib['id'] == 'accessory':
                    body_elements['accessory'] = elem
        
        file_name = os.path.splitext(os.path.basename(body_file))[0]
        svg_cache[file_name] = body_elements

    # Process hair SVGs
    hair_files = glob.glob(os.path.join(hair_svgs_dir, 'Hair*.svg'))
    # Debug: Print the list of hair files found
    print("Hair files found:", hair_files)

    for hair_file in hair_files:
        tree = ET.parse(hair_file)
        root = tree.getroot()
        
        hair_elements = {'tree': tree, 'hair': None, 'accessory': None}
        
        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'hair':
                    hair_elements['hair'] = elem
                elif elem.attrib['id'] == 'accessory':
                    hair_elements['accessory'] = elem
        
        file_name = os.path.splitext(os.path.basename(hair_file))[0]
        svg_cache[file_name] = hair_elements

    # Save the cache to a file
    with open('svg_cache.pkl', 'wb') as cache_file:
        pickle.dump(svg_cache, cache_file)

if __name__ == '__main__':
    preprocess_svgs()
