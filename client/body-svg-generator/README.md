# Body SVG Color Picker

A utility react app to let me generate a bunch of different variants of the body svg, which will be used in the headshot generator project. This loads the body__clean.svg and lets you change the suit and lapel colors, as well as toggling whether the body has a tie or a bowtie.

## Table of Contents

- [Body SVG Color Picker](#body-svg-color-picker)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
    - [Webpack Configuration](#webpack-configuration)
    - [Package Scripts](#package-scripts)
  - [Scripts](#scripts)
  - [Folder Structure](#folder-structure)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/svg-color-picker.git
   cd svg-color-picker
   ```


2. Install dependencies:
   ```sh
   npm install
   ```

3. Install additional required packages:
   ```sh
   npm install react-app-rewired @svgr/webpack customize-cra
   npm install react-color @types/react-color
   ```
   
## Usage

1. Start the development server:
   ```sh
   npm start
   ```

2. Open your browser and navigate to `http://localhost:3000`.

3. Use the color pickers to change the suit and lapel colors, and toggle between tie and bowtie accessories.

4. Click the "Save" button to download the modified SVG.

## Configuration

### Webpack Configuration

The project uses `react-app-rewired` and `customize-cra` to override the default Create React App webpack configuration.

- `config-overrides.js`:
  ```javascript
  const { override, addWebpackModuleRule } = require('customize-cra');

  console.log("Applying custom webpack configuration...");

  module.exports = override(
    addWebpackModuleRule({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    })
  );
  ```

### Package Scripts

- `package.json`:
  ```json
  {
    "scripts": {
      "start": "react-app-rewired start",
      "build": "react-app-rewired build",
      "test": "react-app-rewired test",
      "eject": "react-scripts eject"
    }
  }
  ```

## Scripts

- `npm start`: Starts the development server.
- `npm build`: Builds the application for production.
- `npm test`: Runs the test suite.
- `npm eject`: Ejects the Create React App configuration.

## Folder Structure

- `src/`
  - `App.tsx`: Main application component.
  - `ColorPicker.tsx`: Component for picking colors and accessories.
  - `ColorPicker.css`: CSS for the ColorPicker component.
  - `TestSVG.tsx`: Test component to verify SVG import.
  - `body__clean.svg`: SVG file to be manipulated.
  - `index.tsx`: Entry point for the React application.
  - `react-app-env.d.ts`: TypeScript definitions for the project.
  - `setupTests.ts`: Setup file for tests.
