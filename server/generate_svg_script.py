from app import generate_svg_headshot

if __name__ == '__main__':
    accessory_color = '#ff0000'  # Example accessory color
    svg_headshot = generate_svg_headshot(accessory_color)
    
    # Save the SVG headshot to a file
    with open('headshot.svg', 'w', encoding="utf-8") as file:
        file.write(svg_headshot)

    print("SVG headshot generated and saved to 'headshot.svg'")
