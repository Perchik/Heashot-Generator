# SVG Headshot Generator

## Overview

This project generates SVG headshots for fictional characters using a Flask server and a React client. The headshots are created by combining pre-defined body and hair SVGs with customizable skin, hair, and accessory colors. 

## Project Structure

```
project-root/
│
├── server/
│   ├── app.py
│   ├── preprocess.py
│   ├── skin_hair_combinations.json
│   ├── svg_cache.pkl
│   ├── body_svgs/
│   │   ├── Body1.svg
│   │   ├── Body2.svg
│   │   ├── ...
│   └── hair_svgs/
│       ├── Hair1.svg
│       ├── Hair2.svg
│       ├── ...
│
├── client/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
│
└── README.md
```

## Server Setup

1. **Navigate to the server directory**:
   ```bash
   cd server
   ```

2. **Install the required packages**:
   ```bash
   pip install flask
   ```

3. **Run the preprocessing script** (if not already run):
   ```bash
   python preprocess.py
   ```

4. **Start the Flask server**:
   ```bash
   python app.py
   ```

## Client Setup

1. **Navigate to the client directory**:
   ```bash
   cd client
   ```

2. **Install the required packages**:
   ```bash
   npm install
   ```

3. **Start the React app**:
   ```bash
   npm start
   ```

## Usage

1. Open your web browser and navigate to `http://localhost:3000`.
2. Click the button to generate an SVG headshot with a red accessory.

## Detailed Explanation

### Server Side

- **`app.py`**: 
  - This is the main Flask application file. It handles POST requests at the `/generate_svg_headshot` endpoint.
  - It checks if the `svg_cache.pkl` exists. If not, it runs `preprocess_svgs()` to create the cache.
  - The `generate_svg_headshot()` function randomly selects skin and hair colors from `skin_hair_combinations.json`, updates the SVGs, and returns the combined SVG.

- **`preprocess.py`**: 
  - This script preprocesses the body and hair SVGs, identifying elements with IDs for skin and accessories, and saves this information in a cache file `svg_cache.pkl`.

- **`skin_hair_combinations.json`**: 
  - A JSON file containing pairs of hex codes for common skin and hair color combinations.

### Client Side

- **`App.js`**: 
  - The main React component. It includes a button to generate a headshot with a specified accessory color and displays the SVG headshot.
  - Uses `fetch` API to send a POST request to the Flask server and receive the generated SVG headshot.

- **`index.js`**: 
  - The entry point for the React application.

## Example React Client Code

Here is an example of how the client code can make a request to the Flask server:

```javascript
import React, { useState } from 'react';

const App = () => {
  const [svgHeadshot, setSvgHeadshot] = useState(null);

  const generateSvgHeadshot = async (accessoryColor) => {
    try {
      const response = await fetch('http://localhost:5000/generate_svg_headshot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ accessory_color: accessoryColor })
      });
      const svgHeadshot = await response.text();
      setSvgHeadshot(svgHeadshot);
    } catch (error) {
      console.error('Error generating SVG headshot:', error);
    }
  };

  return (
    <div>
      <h1>Generate SVG Headshot</h1>
      <button onClick={() => generateSvgHeadshot('#ff0000')}>Generate Red Accessory</button>
      {svgHeadshot && <div dangerouslySetInnerHTML={{ __html: svgHeadshot }} />}
    </div>
  );
};

export default App;
```