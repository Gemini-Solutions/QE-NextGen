import React from "react";
import { Route, Routes } from "react-router-dom";
import FindFeatures from "./components/findFeatures/FindFeatures";
import SelectFeatures from "./components/selectFeature/SelectFeatures";
import CodeGeneration from "./components/codeGeneration/CodeGeneration";

export default function Routing() {
  return (
    <Routes>
      <Route path="/" element={<FindFeatures />} />
      <Route path="/selectFeature" element={<SelectFeatures />} />
      <Route path="/codeGeneration" element={<CodeGeneration />}/>
    </Routes>
  );
}
