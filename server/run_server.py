from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from app import generate_svg_headshot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/generate_svg_headshot', methods=['POST'])
def generate_svg_headshot_route():
    try:
        data = request.get_json()
        if not data or 'accessory_color' not in data:
            return make_response(jsonify({'error': 'Missing accessory_color in request'}), 400)

        accessory_color = data.get('accessory_color', '#000000')
        svg_headshot = generate_svg_headshot(accessory_color)
        response = make_response(svg_headshot)
        response.headers['Content-Type'] = 'image/svg+xml'
        return response
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
