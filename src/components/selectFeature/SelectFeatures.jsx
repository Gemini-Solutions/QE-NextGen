import React, { useState, useEffect } from "react";
import "./SelectFeatures.css";
import SelectFeatureNavbar from "../../helper/navBar/selectFeatureNavbar/SelectFeatureNavbar";
import { MenuItem, Select } from "@mui/material";
import SelectInput from "@mui/material/Select/SelectInput";

export default function SelectFeatures() {
  const [features, setFeatures] = useState([]);
  const [firstFour, setFirstFour] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState("");

  useEffect(() => {
    const savedFeatures = JSON.parse(localStorage.getItem("features")) || [];
    setFeatures(savedFeatures);
    const firstFour = savedFeatures.slice(0, 4);
    setFirstFour(firstFour);
  }, []);

  const handleSelection = (event) => {
    setSelectedFeature(event.target.value);
  };

  return (
    <div className="main">
      <SelectFeatureNavbar />
      <h1 className="find-features-heading">Select Features</h1>
      <div className="feature-suggestions">
        {firstFour.length > 0
          ? firstFour.map((feature, index) => (
              <div key={index} className="feature-capsule">
                {feature.heading}
              </div>
            ))
          : "No features available"}
      </div>
      <div className="feature-selection">
        <p className="enter-para">
          Select Feature to Summarize
          <span className="mandatory">*</span>
        </p>
        <Select
          className="features-dropdown"
          onChange={handleSelection}
          value={selectedFeature}
          displayEmpty
        >
          <MenuItem value="" disabled>
            Select
          </MenuItem>
          {features.map((feature, index) => (
            <MenuItem key={index} value={feature.heading}>
              {feature.heading}
            </MenuItem>
          ))}
        </Select>
      </div>
    </div>
  );
}
