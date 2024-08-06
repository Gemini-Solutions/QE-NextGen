import React from "react";
import { ReactSVG } from "react-svg";
import navBarArrow from "../../../assets/navBarArrow.svg";
import "./CodeGenerationNavbar.css";
import { Link } from "react-router-dom";

export default function CodeGenerationNavbar() {
  return (
    <div className="navbar">
      <Link to="/">
        <div className="navbar-box sf-box1">
          <div className="navbar-number sf-number1">01</div>
          <h4 className="navbar-heading">Find Feature</h4>
        </div>
      </Link>
      <ReactSVG src={navBarArrow} className="navBar-arrow" />

      <Link to="/selectFeature">
        <div className="navbar-box box2">
          <div className="navbar-number number2">02</div>
          <h4 className="navbar-heading">Select Feature</h4>
        </div>
      </Link>
      <ReactSVG src={navBarArrow} className="navBar-arrow arrow2" />

      <Link to="/codeGeneration">
        <div className="navbar-box cd-box3">
          <div className="navbar-number cd-number3">03</div>
          <h4 className="navbar-heading">Code Generation</h4>
        </div>
      </Link>
    </div>
  );
}
