import os
import random
import json
import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass

# Configuration
HEX_CODES = [
    "#f94144", "#f3722c", "#f9c74f", "#90be6d", "#43aa8b",
    "#277da1", "#5d4f92", "#ff91af", "#c0c0c0", "#111111"
]
BODY_SVG_DIR = 'body_svgs'
HAIR_SVG_DIR = 'hair_svgs'
SKIN_HAIR_COMBINATIONS_FILE = 'skin_hair_combinations.json'
OUTPUT_FILE = 'random_headshot.svg'


@dataclass
class ColorConfig:
    skin_color: str
    hair_color: str
    accessory_color: str


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
            tree = ET.parse(filepath)
            svg_files[filename] = tree
    return svg_files


def apply_body_colors(tree, colors: ColorConfig):
    """
    Apply colors to the body SVG elements.

    Parameters:
    tree (ElementTree): The SVG tree to apply colors to.
    colors (ColorConfig): The color configuration.

    Raises:
    ValueError: If required elements (skin) are not found.
    """
    ns = {'svg': "http://www.w3.org/2000/svg"}  # Define the namespace
    root = tree.getroot()
    skin = root.find(".//*[@id='Head']", ns)

    paths = root.findall(".//svg:path", ns)
    accessories = [elem for elem in paths if elem.get(
        'id') in {'Tie', 'TieKnot', 'Bowtie'}]

    if skin is not None:
        skin.attrib['fill'] = colors.skin_color
    else:
        raise ValueError("Skin element not found")

    if not accessories:
        logger.debug("No accessories found")
    else:
        for accessory in accessories:
            logger.debug("Setting accessory %s fill to %s",
                         accessory.attrib.get('id'), colors.accessory_color)
            accessory.attrib['fill'] = colors.accessory_color


def apply_hair_colors(tree, colors: ColorConfig):
    """
    Apply colors to the hair SVG elements.

    Parameters:
    tree (ElementTree): The SVG tree to apply colors to.
    colors (ColorConfig): The color configuration.

    Raises:
    ValueError: If required elements (hair) are not found.
    """
    ns = {'svg': "http://www.w3.org/2000/svg"}  # Define the namespace
    root = tree.getroot()
    hair = root.find(".//*[@id='hair']", ns)
    accessories = root.findall(".//*[@id='accessory']", ns)

    if hair is not None:
        hair.attrib['fill'] = colors.hair_color
    else:
        raise ValueError("Hair element not found")

    if not accessories or len(accessories) == 0:
        logger.debug("No accessories found in hair")
    else:
        for accessory in accessories:
            logger.debug("Setting accessory %s fill to %s",
                         accessory.attrib.get('id'), colors.accessory_color)
            accessory.attrib['fill'] = colors.accessory_color


def generate_svg(body_svg, hair_svg, description, colors: ColorConfig):
    """
    Generate a combined SVG headshot.

    Parameters:
    body_svg (ElementTree): The SVG tree for the body.
    hair_svg (ElementTree): The SVG tree for the hair.
    description (str): Description of the combination.
    colors (ColorConfig): The color configuration.

    Returns:
    str: The combined SVG as a string, or None if an error occurs.
    """
    try:
        # Apply colors to the SVG elements
        apply_body_colors(body_svg, colors)
        apply_hair_colors(hair_svg, colors)

        # Create a new combined SVG element
        combined_svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")

        # Copy attributes from the body SVG to the combined SVG
        for attr, value in body_svg.getroot().attrib.items():
            combined_svg.set(attr, value)

        # Add a comment with the description and accessory color
        combined_svg.insert(0, ET.Comment(f'{description}'))

        # Append body and hair elements to the combined SVG
        for child in body_svg.getroot():
            combined_svg.append(child)
        for child in hair_svg.getroot():
            combined_svg.append(child)

        # Return the combined SVG as a string
        return ET.tostring(combined_svg, encoding='unicode')

    except Exception as e:
        logger.error("Error generating SVG headshot: %s", e)
        return None


def generate_random_svg(body_svgs, hair_svgs, skin_hair_combinations, accessory_color):
    """
    Generate a single random SVG headshot.

    Parameters:
    body_svgs (dict): A dictionary of body SVG trees.
    hair_svgs (dict): A dictionary of hair SVG trees.
    skin_hair_combinations (list): A list of lists, each containing skin color, hair color, and description.
    accessory_color (str): The color to apply to the accessory elements.

    Returns:
    str: The combined SVG as a string, or None if an error occurs.
    """
    skin_hair_combo = random.choice(skin_hair_combinations)
    skin_color, hair_color, description = skin_hair_combo

    body_id = random.choice(list(body_svgs.keys()))
    hair_id = random.choice(list(hair_svgs.keys()))
    description += f" {body_id} x {hair_id}"
    return generate_svg(body_svgs[body_id], hair_svgs[hair_id], description, ColorConfig(skin_color, hair_color, accessory_color))


if __name__ == '__main__':
    setup_directory()
    body_svgs = load_svgs(BODY_SVG_DIR, 'Body')
    hair_svgs = load_svgs(HAIR_SVG_DIR, 'Hair')

    with open(SKIN_HAIR_COMBINATIONS_FILE, 'r', encoding="utf-8") as json_file:
        skin_hair_combinations = json.load(json_file)

    svg_headshot = generate_random_svg(
        body_svgs, hair_svgs, skin_hair_combinations, random.choice(HEX_CODES))
    if svg_headshot:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            file.write(svg_headshot)
        logger.info(
            "Random SVG headshot generated and saved to %s", OUTPUT_FILE)
    else:
        logger.error("Failed to generate random SVG headshot")
