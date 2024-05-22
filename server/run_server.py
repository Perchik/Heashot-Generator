from flask import Flask, request, make_response
from app import generate_svg_headshot  

app = Flask(__name__)


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
