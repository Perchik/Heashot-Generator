import os
import random
import pickle
import xml.etree.ElementTree as ET
import json
from preprocess import preprocess_svgs  # Import the preprocess function

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Check if cache exists, if not run preprocessing
if not os.path.exists('svg_cache.pkl'):
    preprocess_svgs()

# Load the SVG cache
with open('svg_cache.pkl', 'rb') as cache_file:
    svg_cache = pickle.load(cache_file)

# Load skin and hair color combinations from JSON file
with open('skin_hair_combinations.json', 'r') as json_file:
    skin_hair_combinations = json.load(json_file)


def generate_svg_headshot(accessory_color):
    # Randomly choose skin and hair color
    skin_color, hair_color, _ = random.choice(skin_hair_combinations)

    # Randomly choose body and hair SVG identifiers
    body_id = random.choice(
        [key for key in svg_cache.keys() if key.startswith('Body')])
    hair_id = random.choice(
        [key for key in svg_cache.keys() if key.startswith('Hair')])

    # Get the SVG elements from the cache
    body_elements = svg_cache[body_id]
    hair_elements = svg_cache[hair_id]

    # Update skin and accessory colors in the body SVG
    if body_elements['skin'] is not None:
        body_elements['skin'].attrib['fill'] = skin_color

       # Update accessory colors in the body SVG
    for accessory in body_elements['accessories']:
        accessory.attrib['fill'] = accessory_color

    # Update hair and accessory colors in the hair SVG
    if hair_elements['hair'] is not None:
        hair_elements['hair'].attrib['fill'] = hair_color
    if hair_elements['accessory'] is not None:
        hair_elements['accessory'].attrib['fill'] = accessory_color

    # Combine body and hair SVGs
    combined_svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")

    for child in body_elements['tree'].getroot():
        combined_svg.append(child)

    for child in hair_elements['tree'].getroot():
        combined_svg.append(child)

    # Convert combined SVG to string
    combined_svg_str = ET.tostring(combined_svg).decode('utf-8')

    return combined_svg_str


if __name__ == '__main__':
    # This section is for generating a single SVG without starting the server
    generate_single_svg = True

    if generate_single_svg:
        accessory_color = '#4ec764'  # Example accessory color
        svg_headshot = generate_svg_headshot(accessory_color)

        # Save the SVG headshot to a file
        with open('headshot.svg', 'w', encoding='utf-8') as file:
            file.write(svg_headshot)

        print("SVG headshot generated and saved to 'headshot.svg'")
