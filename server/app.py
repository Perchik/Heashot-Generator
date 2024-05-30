import os
import random
import json
import logging
import argparse
import gc
from copy import deepcopy
from lxml import etree as ET

HEX_CODES = [
    "#f94144", "#f3722c", "#f9c74f", "#90be6d", "#43aa8b",
    "#277da1", "#5d4f92", "#ff91af", "#c0c0c0", "#111111"
]

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def setup_directory():
    """Set the working directory to the script's directory."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load_svgs(directory):
    """Load and categorize SVGs from a directory."""
    svg_files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            file_path = os.path.join(directory, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()
            body_elements = {'tree': tree, 'skin': None, 'accessories': []}
            for elem in root.iter():
                if 'id' in elem.attrib:
                    if elem.attrib['id'] == 'Head':
                        body_elements['skin'] = elem
                    elif elem.attrib['id'] in ['Tie', 'TieKnot', 'Bowtie']:
                        body_elements['accessories'].append(elem)
                    elif elem.attrib['id'] == 'hair':
                        body_elements['hair'] = elem
                    elif elem.attrib['id'] == 'accessory':
                        body_elements['accessory'] = elem
            svg_files[filename] = body_elements
    return svg_files


def load_skin_hair_combinations():
    """Load skin and hair color combinations from JSON file."""
    with open('skin_hair_combinations.json', 'r') as json_file:
        return json.load(json_file)


def generate_svg_headshot(skin_color, hair_color, description, body_elements, hair_elements, accessory_color='#4ec764'):
    """Generate a combined SVG headshot."""
    try:

        if not body_elements or not hair_elements:
            raise ValueError("Missing body or hair elements")

        # Update colors
        if body_elements['skin'] is not None:
            body_elements['skin'].attrib['fill'] = skin_color
        else:
            raise ValueError("Skin element not found in body elements")

        for accessory in body_elements['accessories']:
            accessory.attrib['fill'] = accessory_color

        if hair_elements['hair'] is not None:
            hair_elements['hair'].attrib['fill'] = hair_color
        else:
            raise ValueError("Hair element not found in hair elements")

        if 'accessory' in hair_elements:
            hair_elements['accessory'].attrib['fill'] = accessory_color

        # Create combined SVG
        combined_svg = ET.Element(
            'svg', nsmap={None: "http://www.w3.org/2000/svg"})
        for attr, value in body_elements['tree'].getroot().attrib.items():
            combined_svg.set(attr, value)

        description = description.replace('skin', f'skin ({skin_color})').replace(
            'hair', f'hair ({hair_color})')
        combined_svg.insert(0, ET.Comment(
            f'{description} with {accessory_color} accessory'))

        for child in list(body_elements['tree'].getroot()):
            combined_svg.append(child)

        for child in list(hair_elements['tree'].getroot()):
            combined_svg.append(child)

        return ET.tostring(combined_svg, pretty_print=True, encoding='unicode')

    except Exception as e:
        logger.error("Error generating SVG headshot: %s", e)
        return None


def save_svgs(body_svgs, hair_svgs, skin_hair_combinations):
    """Generate and save all possible SVG combinations."""
    output_dir = 'generated_svgs'
    os.makedirs(output_dir, exist_ok=True)

    body_ids = list(body_svgs.keys())
    hair_ids = list(hair_svgs.keys())

    count = 0
    for skin_color, hair_color, description in skin_hair_combinations:
        body_id = body_ids[count % len(body_ids)]
        hair_id = hair_ids[count % len(hair_ids)]

        logger.info(f"Generating SVG {count + 1} for body_id: {body_id}, hair_id: {
                    hair_id}, skin_color: {skin_color}, hair_color: {hair_color}")

        svg_headshot = generate_svg_headshot(
            skin_color, hair_color, description, body_svgs[body_id], hair_svgs[hair_id])
        if svg_headshot:
            file_name = f'svg_{count}.svg'
            with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
                file.write(svg_headshot)
            count += 1
            gc.collect()
        else:
            logger.warning(f"Failed to generate SVG for body_id: {
                           body_id}, hair_id: {hair_id}")

    logger.info(f"Generated {count} SVG files")


def generate_random_svg(body_svgs, hair_svgs, skin_hair_combinations, accessory_color):
    """Generate a single random SVG headshot."""
    skin_color, hair_color, description = random.choice(skin_hair_combinations)
    body_id = random.choice(list(body_svgs.keys()))
    hair_id = random.choice(list(hair_svgs.keys()))
    return generate_svg_headshot(skin_color, hair_color, description, body_svgs[body_id], hair_svgs[hair_id], accessory_color)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate SVG headshots.')
    parser.add_argument('--all', action='store_true',
                        help='Generate all possible SVG combinations')
    parser.add_argument('--random', action='store_true',
                        help='Generate a single random SVG')

    args = parser.parse_args()

    setup_directory()
    body_svgs = load_svgs('body_svgs')
    hair_svgs = load_svgs('hair_svgs')
    skin_hair_combinations = load_skin_hair_combinations()

    if args.all:
        save_svgs(body_svgs, hair_svgs, skin_hair_combinations)
    elif args.random:
        svg_headshot = generate_random_svg(
            body_svgs, hair_svgs, skin_hair_combinations, random.choice(HEX_CODES))
        if svg_headshot:
            with open('random_headshot.svg', 'w', encoding='utf-8') as file:
                file.write(svg_headshot)
            logger.info(
                "Random SVG headshot generated and saved to 'random_headshot.svg'")
        else:
            logger.error("Failed to generate random SVG headshot")
    else:
        parser.print_help()
