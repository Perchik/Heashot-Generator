import React, { useState, useEffect } from "react";
import { SketchPicker, ColorResult } from "react-color";
import { default as BodySVG } from "./SvgComponent"; // Importing SvgComponent as BodySVG
import "./ColorPicker.css";

const ColorPicker: React.FC = () => {
  const [selectedColor, setSelectedColor] = useState<string>("#000000");
  const [selectedPart, setSelectedPart] = useState<string>("Suit");
  const [suitColor, setSuitColor] = useState<string>("#000000");
  const [lapelColor, setLapelColor] = useState<string>("#000000");
  const [shirtColor, setShirtColor] = useState<string>("#FFFFFF");
  const [accessory, setAccessory] = useState<string>("Tie");
  const [recentColors, setRecentColors] = useState<string[]>([]);

  useEffect(() => {
    const tieElement = document.getElementById("Tie");
    const bowtieElement = document.getElementById("Bowtie");
    if (tieElement)
      tieElement.style.display = accessory === "Tie" ? "inline" : "none";
    if (bowtieElement)
      bowtieElement.style.display = accessory === "Bowtie" ? "inline" : "none";
  }, [accessory]);

  useEffect(() => {
    const suitElement = document.getElementById("Suit");
    if (suitElement) suitElement.style.fill = suitColor;
  }, [suitColor]);

  useEffect(() => {
    const lapelElement = document.getElementById("Lapel");
    if (lapelElement) lapelElement.style.fill = lapelColor;
  }, [lapelColor]);

  useEffect(() => {
    const shirtElement = document.getElementById("Shirt");
    if (shirtElement) shirtElement.style.fill = shirtColor;
  }, [shirtColor]);

  const handleAccessoryChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setAccessory(event.target.value);
  };

  const handleSave = () => {
    const svg = document.getElementById("body-svg");
    if (!svg) return;

    const svgData = new XMLSerializer().serializeToString(svg);
    const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "modified_body.svg";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleSetColor = () => {
    switch (selectedPart) {
      case "Suit":
        setSuitColor(selectedColor);
        break;
      case "Lapels":
        setLapelColor(selectedColor);
        break;
      case "Shirt":
        setShirtColor(selectedColor);
        break;
      default:
        const element = document.getElementById(selectedPart);
        if (element) {
          element.style.fill = selectedColor;
        }
        break;
    }
    if (!recentColors.includes(selectedColor)) {
      setRecentColors([selectedColor, ...recentColors].slice(0, 5));
    }
  };

  const handleColorChange = (color: ColorResult) => {
    setSelectedColor(color.hex);
    switch (selectedPart) {
      case "Suit":
        const suitElement = document.getElementById("Suit");
        if (suitElement) suitElement.style.fill = color.hex;
        break;
      case "Lapels":
        const lapelElement = document.getElementById("Lapel");
        if (lapelElement) lapelElement.style.fill = color.hex;
        break;
      case "Shirt":
        const shirtElement = document.getElementById("Shirt");
        if (shirtElement) shirtElement.style.fill = color.hex;
        break;
      default:
        const element = document.getElementById(selectedPart);
        if (element) {
          element.style.fill = color.hex;
        }
        break;
    }
  };

  return (
    <div className="color-picker-container">
      <div className="svg-container">
        <BodySVG id="body-svg" />
      </div>
      <div className="controls-container">
        <div className="part-picker">
          <h3>Select Part</h3>
          <select
            value={selectedPart}
            onChange={(e) => setSelectedPart(e.target.value)}
          >
            <option value="Suit">Suit</option>
            <option value="Lapels">Lapels</option>
            <option value="Shirt">Shirt</option>
          </select>
        </div>
        <div className="color-picker">
          <h3>Select Color</h3>
          <SketchPicker
            color={selectedColor}
            onChange={handleColorChange}
            presetColors={recentColors}
          />
        </div>
        <button onClick={handleSetColor}>Set Color</button>
        <div className="accessory-picker">
          <h3>Select Accessory</h3>
          <label>
            <input
              type="radio"
              value="Tie"
              checked={accessory === "Tie"}
              onChange={handleAccessoryChange}
            />
            Tie
          </label>
          <label>
            <input
              type="radio"
              value="Bowtie"
              checked={accessory === "Bowtie"}
              onChange={handleAccessoryChange}
            />
            Bowtie
          </label>
        </div>
        <button onClick={handleSave}>Save</button>
      </div>
    </div>
  );
};

export default ColorPicker;
