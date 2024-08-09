import React, { useEffect, useState } from "react";
import CodeGenerationNavbar from "../../helper/navBar/codeGeneration/CodeGenerationNavbar";
import { MenuItem, Select } from "@mui/material";
import CodeMirror from "@uiw/react-codemirror";
import { basicSetup } from "codemirror";
import { java } from "@codemirror/lang-java";
import { ReactSVG } from "react-svg";
import copy from "../../assets/copy.svg";
import "./CodeGeneration.css";
import "../selectFeature/SelectFeatures.css";

export default function CodeGeneration() {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState("");
  const [stepDefCopied, setStepDefCopied] = useState(false);
  const [impCopied, setImpCopied] = useState(false);
  const [locCopied, setLocCopied] = useState(false);
  const [stepDefContent, setStepDefContent] = useState("");
  const [implementationContent, setImplementationContent] = useState("");
  const [locatorContent, setLocatorContent] = useState("");

  useEffect(() => {
    const savedScenarios = JSON.parse(localStorage.getItem("scenarios")) || [];
    setScenarios(savedScenarios);
    console.log(savedScenarios);
  }, []);

  const handleChange = async (event) => {
    const scenarioName = event.target.value;
    setSelectedScenario(scenarioName);

    const selectedScenario = scenarios.find(
      (scenario) => scenario.scenarioName === scenarioName
    );

    if (selectedScenario) {
      try {
        const stepDefRes = await fetch(selectedScenario.stepDef);
        const implementationRes = await fetch(selectedScenario.implementation);
        const locatorsRes = await fetch(selectedScenario.locators);

        if (stepDefRes.ok && implementationRes.ok && locatorsRes.ok) {
          const stepDefText = await stepDefRes.text();
          const implementationText = await implementationRes.text();
          const locatorsText = await locatorsRes.text();

          setStepDefContent(stepDefText);
          setImplementationContent(implementationText);
          setLocatorContent(locatorsText);
        } else {
          console.error("Failed to fetch one or more files");
        }
      } catch (e) {
        console.error("Failed to load files", e);
      }
    }
  };

  const copyStepDefContent = (content) => {
    navigator.clipboard
      .writeText(content)
      .then(() => {
        setStepDefCopied(true);
        setTimeout(() => setStepDefCopied(false), 2000);
        console.log("copied");
      })
      .catch((err) => {
        console.error("failed to copy", err);
      });
  };

  const copyImpContent = (content) => {
    navigator.clipboard
      .writeText(content)
      .then(() => {
        setImpCopied(true);
        setTimeout(() => setImpCopied(false), 2000);
        console.log("copied");
      })
      .catch((err) => {
        console.error("failed to copy", err);
      });
  };

  const copyLocContent = (content) => {
    navigator.clipboard
      .writeText(content)
      .then(() => {
        setLocCopied(true);
        setTimeout(() => setLocCopied(false), 2000);
        console.log("copied");
      })
      .catch((err) => {
        console.error("failed to copy", err);
      });
  };

  return (
    <div className="main">
      <CodeGenerationNavbar />
      <h1 className="find-features-heading">Code Generation</h1>
      <div className="scenario-selection">
        <p className="enter-para">
          Select Scenario to Generate Code<span className="mandatory">*</span>
        </p>
        <Select
          className="scenario-dropdown"
          value={selectedScenario}
          onChange={handleChange}
          displayEmpty
        >
          <MenuItem value="" disabled>
            Select scenario
          </MenuItem>
          {scenarios.map((scenario, index) => (
            <MenuItem
              key={index}
              value={scenario.scenarioName}
              className="scenario-dropdown-item"
            >
              {scenario.scenarioName}
            </MenuItem>
          ))}
        </Select>
      </div>
      {selectedScenario && (
        <>
          <p className="feature-file-heading">StepDefinition File</p>
          <div className="editor-container">
            <CodeMirror
              value={stepDefContent}
              className="code-editor"
              height="29.875rem"
              extensions={[basicSetup, java()]}
              basicSetup={{
                lineNumbers: true,
                foldGutter: true,
                highlightActiveLine: true,
                highlightActiveLineGutter: true,
                lineWrapping: true,
              }}
            />
            <button
              onClick={() => copyStepDefContent(stepDefContent)}
              className="copy"
            >
              <ReactSVG src={copy} />
            </button>
            {stepDefCopied && <p className="copied-message">Copied!</p>}
          </div>

          <p className="feature-file-heading">Implementation File</p>
          <div className="editor-container">
            <CodeMirror
              value={implementationContent}
              className="code-editor"
              height="29.875rem"
              extensions={[basicSetup, java()]}
              basicSetup={{
                lineNumbers: true,
                foldGutter: true,
                highlightActiveLine: true,
                highlightActiveLineGutter: true,
                lineWrapping: true,
              }}
            />
            <button
              onClick={() => copyImpContent(implementationContent)}
              className="copy"
            >
              <ReactSVG src={copy} />
            </button>
            {impCopied && <p className="copied-message">Copied!</p>}
          </div>

          <p className="feature-file-heading">Locator File</p>
          <div className="editor-container">
            <CodeMirror
              value={locatorContent}
              className="code-editor"
              height="29.875rem"
              extensions={[basicSetup, java()]}
              basicSetup={{
                lineNumbers: true,
                foldGutter: true,
                highlightActiveLine: true,
                highlightActiveLineGutter: true,
                lineWrapping: true,
              }}
            />
            <button
              onClick={() => copyLocContent(locatorContent)}
              className="copy loc-copy"
            >
              <ReactSVG src={copy} />
            </button>
            {locCopied && <p className="copied-message">Copied!</p>}
          </div>
        </>
      )}
    </div>
  );
}
