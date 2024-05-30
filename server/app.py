import os
import random
import pickle
import json
import logging
import argparse
from lxml import etree as ET
from preprocess import preprocess_svgs

HEX_CODES = [
    "#f94144",
    "#f3722c",
    "#f9c74f",
    "#90be6d",
    "#43aa8b",
    "#277da1",
    "#5d4f92",
    "#ff91af",
    "#c0c0c0",
    "#111111"
]

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

logger.debug("Starting script execution...")

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Check if cache exists, if not run preprocessing
if not os.path.exists('svg_cache.pkl'):
    logger.info("svg_cache.pkl not found. Running preprocessing...")
    preprocess_svgs()

# Load the SVG cache
logger.info("Loading SVG cache...")
with open('svg_cache.pkl', 'rb') as cache_file:
    svg_cache = pickle.load(cache_file)

# Convert string representations back to ElementTree objects
logger.info("Converting string representations back to ElementTree objects...")
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
        logger.error(
            "Error converting string to ElementTree for key %s: %s", key, e)

# Load skin and hair color combinations from JSON file
logger.info("Loading skin and hair color combinations from JSON file...")
with open('skin_hair_combinations.json', 'r') as json_file:
    skin_hair_combinations = json.load(json_file)


def generate_svg_headshot(skin_color, hair_color, description, body_id, hair_id, accessory_color='#4ec764'):
    try:
        # Get the SVG elements from the cache
        body_elements = svg_cache[body_id]
        hair_elements = svg_cache[hair_id]

        # Update skin and accessory colors in the body SVG
        if body_elements.get('skin') is not None:
            body_elements['skin'].attrib['fill'] = skin_color
        else:
            logger.warning("Skin element not found in body elements")

        # Update accessory colors in the body SVG
        for accessory in body_elements.get('accessories', []):
            accessory.attrib['fill'] = accessory_color

        # Update hair and accessory colors in the hair SVG
        if hair_elements.get('hair') is not None:
            hair_elements['hair'].attrib['fill'] = hair_color
        else:
            logger.warning("Hair element not found in hair elements")

        if hair_elements.get('accessory') is not None:
            hair_elements['accessory'].attrib['fill'] = accessory_color

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
        logger.error("Error generating SVG headshot: %s", e)
        return None


def save_svgs():
    logger.info("Saving all possible SVG combinations...")
    output_dir = 'generated_svgs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    body_ids = [key for key in svg_cache.keys() if key.startswith('Body')]
    hair_ids = [key for key in svg_cache.keys() if key.startswith('Hair')]

    body_iter = iter(body_ids)
    hair_iter = iter(hair_ids)

    count = 0
    for skin_color, hair_color, description in skin_hair_combinations:
        try:
            body_id = next(body_iter)
        except StopIteration:
            body_iter = iter(body_ids)
            body_id = next(body_iter)

        try:
            hair_id = next(hair_iter)
        except StopIteration:
            hair_iter = iter(hair_ids)
            hair_id = next(hair_iter)

        svg_headshot = generate_svg_headshot(
            skin_color, hair_color, description, body_id, hair_id)
        if svg_headshot:
            file_name = f'svg_{count}.svg'
            with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
                file.write(svg_headshot)
            count += 1
    logger.info(f"Generated {count} SVG files")


def generate_random_svg(accessory_color):
    logger.info("Generating a random SVG headshot...")
    skin_color, hair_color, description = random.choice(skin_hair_combinations)
    body_id = random.choice(
        [key for key in svg_cache.keys() if key.startswith('Body')])
    hair_id = random.choice(
        [key for key in svg_cache.keys() if key.startswith('Hair')])
    return generate_svg_headshot(skin_color, hair_color, description, body_id, hair_id, accessory_color)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate SVG headshots.')
    parser.add_argument('--all', action='store_true',
                        help='Generate all possible SVG combinations')
    parser.add_argument('--random', action='store_true',
                        help='Generate a single random SVG')

    args = parser.parse_args()

    logger.debug("Parsed arguments: %s", args)

    if args.all:
        save_svgs()
    elif args.random:
        logger.info("Random flag detected, generating random SVG...")
        svg_headshot = generate_random_svg(random.choice(HEX_CODES))
        if svg_headshot:
            with open('random_headshot.svg', 'w', encoding='utf-8') as file:
                file.write(svg_headshot)
            logger.info(
                "Random SVG headshot generated and saved to 'random_headshot.svg'")
        else:
            logger.error("Failed to generate random SVG headshot")
    else:
        parser.print_help()
