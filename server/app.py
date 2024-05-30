import os
import random
import pickle
import json
import logging
from lxml import etree as ET
from preprocess import preprocess_svgs

# Set up logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Check if cache exists, if not run preprocessing
if not os.path.exists('svg_cache.pkl'):
    logging.info("svg_cache.pkl not found. Running preprocessing...")
    preprocess_svgs()

# Load the SVG cache
with open('svg_cache.pkl', 'rb') as cache_file:
    svg_cache = pickle.load(cache_file)

# Convert string representations back to ElementTree objects
for key, value in svg_cache.items():
    try:
        tree = ET.ElementTree(ET.fromstring(value['tree']))
        value['tree'] = tree
        if value.get('skin') is not None:
            value['skin'] = tree.find(f".//*[@id='{value['skin']}']")
        value['accessories'] = [
            tree.find(f".//*[@id='{acc}']") for acc in value.get('accessories', [])]
        if value.get('hair') is not None:
            value['hair'] = tree.find(f".//*[@id='{value['hair']}']")
        if value.get('accessory') is not None:
            value['accessory'] = tree.find(f".//*[@id='{value['accessory']}']")
    except Exception as e:
        logging.error(
            "Error converting string to ElementTree for key %s: %s", key, e)

# Load skin and hair color combinations from JSON file
with open('skin_hair_combinations.json', 'r') as json_file:
    skin_hair_combinations = json.load(json_file)


def generate_svg_headshot(accessory_color):
    try:
        # Randomly choose skin and hair color
        skin_color, hair_color, description = random.choice(
            skin_hair_combinations)

        # Randomly choose body and hair SVG identifiers
        body_id = random.choice(
            [key for key in svg_cache.keys() if key.startswith('Body')])
        hair_id = random.choice(
            [key for key in svg_cache.keys() if key.startswith('Hair')])

        # Get the SVG elements from the cache
        body_elements = svg_cache[body_id]
        hair_elements = svg_cache[hair_id]

        # Update skin and accessory colors in the body SVG
        if body_elements.get('skin') is not None:
            body_elements['skin'].attrib['fill'] = skin_color
        else:
            logging.warning("Skin element not found in body elements")

        # Update accessory colors in the body SVG
        for accessory in body_elements.get('accessories', []):
            accessory.attrib['fill'] = accessory_color

        # Update hair and accessory colors in the hair SVG
        if hair_elements.get('hair') is not None:
            hair_elements['hair'].attrib['fill'] = hair_color
        else:
            logging.warning("Hair element not found in hair elements")

        if hair_elements.get('accessory') is not None:
            hair_elements['accessory'].attrib['fill'] = accessory_color
        else:
            logging.warning("Accessory element not found in hair elements")

        # Create a combined SVG root element with proper namespace
        combined_svg = ET.Element(
            'svg', nsmap={None: "http://www.w3.org/2000/svg"})

        description = description.replace('skin', f'skin ({skin_color})').replace(
            'hair', f'hair ({hair_color})')
        generation_comment = ET.Comment(f'{body_id} x {hair_id}, {description} with {
                                        accessory_color} accessory')
        combined_svg.insert(0, generation_comment)

        # Append body and hair elements to the combined SVG
        for child in body_elements['tree'].getroot():
            combined_svg.append(child)

        for child in hair_elements['tree'].getroot():
            combined_svg.append(child)

        # Convert combined SVG to string
        combined_svg_str = ET.tostring(
            combined_svg, pretty_print=True, encoding='unicode')

        return combined_svg_str

    except Exception as e:
        logging.error("Error generating SVG headshot: %s", e)
        return None


if __name__ == '__main__':
    accessory_color = '#4ec764'  # Example accessory color
    svg_headshot = generate_svg_headshot(accessory_color)

    if svg_headshot:
        # Save the SVG headshot to a file
        with open('headshot.svg', 'w', encoding='utf-8') as file:
            file.write(svg_headshot)
        logging.info("SVG headshot generated and saved to 'headshot.svg'")
    else:
        logging.error("Failed to generate SVG headshot")
