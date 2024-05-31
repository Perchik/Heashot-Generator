import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from headshot_generator import generate_headshot, HEX_CODES, setup_directory

app = Flask(__name__)
CORS(app)  # Enable CORS


@app.route('/generate_headshot', methods=['POST'])
def generate_headshot_endpoint():
    data = request.json
    accessory_color = data.get('accessory_color', random.choice(HEX_CODES))
    svg_headshot = generate_headshot(accessory_color)
    if svg_headshot:
        return jsonify({'svg': svg_headshot}), 200
    else:
        return jsonify({'error': 'Failed to generate SVG headshot'}), 500


if __name__ == '__main__':
    setup_directory()
    app.run(host='0.0.0.0', port=5000)
