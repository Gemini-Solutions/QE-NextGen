import React, { useState, useEffect, useRef } from "react";
import "./SelectFeatures.css";
import SelectFeatureNavbar from "../../helper/navBar/selectFeatureNavbar/SelectFeatureNavbar";
import { MenuItem, Select } from "@mui/material";
import CodeMirror from "@uiw/react-codemirror";
import { ReactSVG } from "react-svg";
import copy from "../../assets/copy.svg";
import scenarioData from "../codeGeneration/scenarioData";

export default function SelectFeatures() {
  const [features, setFeatures] = useState([]);
  const [firstFour, setFirstFour] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [featureFileContent, setFeatureFileContent] = useState("");
  const [summary, setSummary] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const savedFeatures = JSON.parse(localStorage.getItem("features")) || [];
    setFeatures(savedFeatures);
    setFirstFour(savedFeatures.slice(0, 4));
  }, []);

  useEffect(() => {
    if (selectedFeature) {
      setSummary(selectedFeature.summary);
    }
  }, [selectedFeature]);

  const handleSummaryChange = (event) => {
    setSummary(event.target.value);
  };

  const handleSelection = async (event) => {
    const selectedHeading = event.target.value;
    const feature = features.find((f) => f.heading === selectedHeading);
    setSelectedFeature(feature);
    localStorage.setItem("scenarios", JSON.stringify(scenarioData));

    if (feature) {
      try {
        const response = await fetch(feature.featureFile);
        if (response.ok) {
          const text = await response.text();
          setFeatureFileContent(text);
        }
      } catch (error) {
        console.error("Error fetching the feature file:", error);
        setFeatureFileContent("Error loading feature file content");
      }
    }
  };

  const copyContent = () => {
    navigator.clipboard
      .writeText(featureFileContent)
      .then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
        console.log("copied");
      })
      .catch((err) => {
        console.error("failed to copy", err);
      });
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
          value={selectedFeature ? selectedFeature.heading : ""}
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
        {selectedFeature && (
          <>
            <p className="enter-para" style={{ marginTop: "1.5%" }}>
              Code block summary
            </p>
            <textarea
              className="feature-summary"
              value={summary}
              onChange={handleSummaryChange}
            />
            <p className="feature-file-heading">Feature File</p>
            <div className="editor-container">
              <CodeMirror
                value={featureFileContent}
                height="29.875rem"
                className="code-editor"
                options={{
                  mode: "text",
                  theme: "default",
                  lineNumbers: true,
                }}
              />
              <button onClick={copyContent} className="copy">
                <ReactSVG src={copy} />
              </button>
              {copied && <p className="copied-message">Copied!</p>}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
