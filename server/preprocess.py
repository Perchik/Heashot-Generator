import pickle
import xml.etree.ElementTree as ET
import os


def preprocess_svgs(body_svgs_dir='body_svgs', hair_svgs_dir='hair_svgs'):
    svg_cache = {}

    # Process body SVGs
    for i in range(1, 13):
        body_file = f'{body_svgs_dir}/Body{i}.svg'
        tree = ET.parse(body_file)
        root = tree.getroot()

        body_elements = {'tree': tree, 'skin': None, 'accessory': None}

        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'skin':
                    body_elements['skin'] = elem
                elif elem.attrib['id'] == 'accessory':
                    body_elements['accessory'] = elem

        svg_cache[f'Body{i}'] = body_elements

    # Process hair SVGs
    for i in range(1, 17):
        hair_file = f'{hair_svgs_dir}/Hair{i}.svg'
        tree = ET.parse(hair_file)
        root = tree.getroot()

        hair_elements = {'tree': tree, 'hair': None, 'accessory': None}

        for elem in root.iter():
            if 'id' in elem.attrib:
                if elem.attrib['id'] == 'hair':
                    hair_elements['hair'] = elem
                elif elem.attrib['id'] == 'accessory':
                    hair_elements['accessory'] = elem

        svg_cache[f'Hair{i}'] = hair_elements

    # Save the cache to a file
    with open('svg_cache.pkl', 'wb') as cache_file:
        pickle.dump(svg_cache, cache_file)


if __name__ == '__main__':
    preprocess_svgs()
