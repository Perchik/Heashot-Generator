import os
import random
import json
import logging
import argparse
from copy import deepcopy
from lxml import etree as ET

# Configuration
HEX_CODES = [
    "#f94144", "#f3722c", "#f9c74f", "#90be6d", "#43aa8b",
    "#277da1", "#5d4f92", "#ff91af", "#c0c0c0", "#111111"
]
BODY_SVG_DIR = 'body_svgs'
HAIR_SVG_DIR = 'hair_svgs'
SKIN_HAIR_COMBINATIONS_FILE = 'skin_hair_combinations.json'

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def setup_directory():
    """
    Set the working directory to the script's directory.
    This ensures that relative paths are resolved correctly.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load_svgs(svg_dir, prefix):
    """
    Load SVG files from a directory with a specific prefix.

    Parameters:
    svg_dir (str): The directory to load SVG files from.
    prefix (str): The prefix to filter SVG files by.

    Returns:
    dict: A dictionary where keys are filenames and values are parsed SVG trees.
    """
    svg_files = {}
    for filename in os.listdir(svg_dir):
        if filename.startswith(prefix) and filename.endswith('.svg'):
            filepath = os.path.join(svg_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                svg_files[filename] = ET.parse(file)
    return svg_files


def load_skin_hair_combinations(filepath):
    """
    Load skin and hair color combinations from a JSON file.

    Parameters:
    filepath (str): The path to the JSON file.

    Returns:
    list: A list of skin and hair color combinations with descriptions.
    """
    with open(filepath, 'r') as json_file:
        return json.load(json_file)


def apply_body_colors(tree, skin_color, accessory_color):
    """
    Apply colors to the body SVG elements.

    Parameters:
    tree (ElementTree): The SVG tree to apply colors to.
    skin_color (str): The color to apply to the skin elements.
    accessory_color (str): The color to apply to the accessory elements.

    Raises:
    ValueError: If required elements (skin) are not found.
    """
    root = tree.getroot()
    skin = root.find(".//*[@id='Head']")
    accessories = root.findall(
        ".//*[@id='Tie'] | .//*[@id='TieKnot'] | .//*[@id='Bowtie']")

    if skin is not None:
        skin.attrib['fill'] = skin_color
    else:
        raise ValueError("Skin element not found")

    for accessory in accessories:
        accessory.attrib['fill'] = accessory_color


def apply_hair_colors(tree, hair_color, accessory_color):
    """
    Apply colors to the hair SVG elements.

    Parameters:
    tree (ElementTree): The SVG tree to apply colors to.
    hair_color (str): The color to apply to the hair elements.
    accessory_color (str): The color to apply to the accessory elements.

    Raises:
    ValueError: If required elements (hair) are not found.
    """
    root = tree.getroot()
    hair = root.find(".//*[@id='hair']")
    accessories = root.findall(".//*[@id='accessory']")

    if hair is not None:
        hair.attrib['fill'] = hair_color
    else:
        raise ValueError("Hair element not found")

    for accessory in accessories:
        accessory.attrib['fill'] = accessory_color


def generate_svg(body_svg, hair_svg, skin_color, hair_color, description, accessory_color='#4ec764'):
    """
    Generate a combined SVG headshot.

    Parameters:
    body_svg (ElementTree): The SVG tree for the body.
    hair_svg (ElementTree): The SVG tree for the hair.
    skin_color (str): The color to apply to the skin elements.
    hair_color (str): The color to apply to the hair elements.
    description (str): Description of the combination.
    accessory_color (str, optional): The color to apply to the accessory elements. Defaults to '#4ec764'.

    Returns:
    str: The combined SVG as a string, or None if an error occurs.
    """
    try:
        # Deep copy the SVG trees to avoid modifying the originals
        body_svg_copy = deepcopy(body_svg)
        hair_svg_copy = deepcopy(hair_svg)

        # Apply colors to the SVG elements
        apply_body_colors(body_svg_copy, skin_color, accessory_color)
        apply_hair_colors(hair_svg_copy, hair_color, accessory_color)

        # Create a new combined SVG element
        combined_svg = ET.Element(
            'svg', nsmap={None: "http://www.w3.org/2000/svg"})

        # Copy attributes from the body SVG to the combined SVG
        for attr, value in body_svg_copy.getroot().attrib.items():
            combined_svg.set(attr, value)

        # Add a comment with the description and accessory color
        combined_svg.insert(0, ET.Comment(
            f'{description} with {accessory_color} accessory'))

        # Append body and hair elements to the combined SVG
        for child in body_svg_copy.getroot():
            combined_svg.append(child)
        for child in hair_svg_copy.getroot():
            combined_svg.append(child)

        # Return the combined SVG as a string
        return ET.tostring(combined_svg, pretty_print=True, encoding='unicode')

    except Exception as e:
        logger.error("Error generating SVG headshot: %s", e)
        return None


def save_svgs(body_svgs, hair_svgs, skin_hair_combinations):
    """
    Generate and save all possible SVG combinations.

    Parameters:
    body_svgs (dict): A dictionary of body SVG trees.
    hair_svgs (dict): A dictionary of hair SVG trees.
    skin_hair_combinations (list): A list of skin and hair color combinations with descriptions.
    """
    output_dir = 'generated_svgs'
    os.makedirs(output_dir, exist_ok=True)

    body_ids = list(body_svgs.keys())
    hair_ids = list(hair_svgs.keys())

    count = 0
    for skin_color, hair_color, description in skin_hair_combinations:
        body_id = body_ids[count % len(body_ids)]
        hair_id = hair_ids[count % len(hair_ids)]

        svg_headshot = generate_svg(
            body_svgs[body_id], hair_svgs[hair_id], skin_color, hair_color, description)
        if svg_headshot:
            file_name = f'svg_{count}.svg'
            with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
                file.write(svg_headshot)
            count += 1
        else:
            logger.warning(f"Failed to generate SVG for body_id: {
                           body_id}, hair_id: {hair_id}")

    logger.info(f"Generated {count} SVG files")


def generate_random_svg(body_svgs, hair_svgs, skin_hair_combinations, accessory_color):
    """
    Generate a single random SVG headshot.

    Parameters:
    body_svgs (dict): A dictionary of body SVG trees.
    hair_svgs (dict): A dictionary of hair SVG trees.
    skin_hair_combinations (list): A list of skin and hair color combinations with descriptions.
    accessory_color (str): The color to apply to the accessory elements.

    Returns:
    str: The combined SVG as a string, or None if an error occurs.
    """
    skin_color, hair_color, description = random.choice(skin_hair_combinations)
    body_id = random.choice(list(body_svgs.keys()))
    hair_id = random.choice(list(hair_svgs.keys()))
    return generate_svg(body_svgs[body_id], hair_svgs[hair_id], skin_color, hair_color, description, accessory_color)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate SVG headshots.')
    parser.add_argument('--all', action='store_true',
                        help='Generate all possible SVG combinations')
    parser.add_argument('--random', action='store_true',
                        help='Generate a single random SVG')

    args = parser.parse_args()

    setup_directory()
    body_svgs = load_svgs(BODY_SVG_DIR, 'Body')
    hair_svgs = load_svgs(HAIR_SVG_DIR, 'Hair')
    skin_hair_combinations = load_skin_hair_combinations(
        SKIN_HAIR_COMBINATIONS_FILE)

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
