from flask import Flask, request, jsonify, make_response
import random
import pickle
import xml.etree.ElementTree as ET
import json
import os

app = Flask(__name__)

# Preprocess SVG files to create a cache if it doesn't exist


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
    skin_color, hair_color = random.choice(skin_hair_combinations)

    # Randomly choose body and hair SVG identifiers
    body_id = f'Body{random.randint(1, 12)}'
    hair_id = f'Hair{random.randint(1, 16)}'

    # Get the SVG elements from the cache
    body_elements = svg_cache[body_id]
    hair_elements = svg_cache[hair_id]

    # Update skin and accessory colors in the body SVG
    if body_elements['skin'] is not None:
        body_elements['skin'].attrib['fill'] = skin_color
    if body_elements['accessory'] is not None:
        body_elements['accessory'].attrib['fill'] = accessory_color

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


@app.route('/generate_svg_headshot', methods=['POST'])
def generate_svg_headshot_route():
    data = request.get_json()
    # Default to black if not provided
    accessory_color = data.get('accessory_color', '#000000')
    svg_headshot = generate_svg_headshot(accessory_color)
    response = make_response(svg_headshot)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
