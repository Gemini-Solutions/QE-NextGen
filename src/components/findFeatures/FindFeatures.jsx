import React, { useState, useEffect } from "react";
import "./FindFeatures.css";
import FindFeaturesNavbar from "../../helper/navBar/findFeaturesNavbar/FindFeaturesNavbar";
import info from "../../assets/info.svg";
import { ReactSVG } from "react-svg";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Skeleton from "@mui/material/Skeleton";
import featuresData from "./featuresData";
import Pagination from "../../helper/pagination/Pagination";

export default function FindFeatures() {
  const [isSelected, setIsSelected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");
  const [features, setFeatures] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const featuresPerPage = 6;

  useEffect(() => {
    setFeatures([]);
    setCurrentPage(1);
  }, [isSelected]);

  const handleSelection = (event) => {
    setIsSelected(event.target.value);
  };

  const handleEnterPress = (e) => {
    if (e.key === "Enter") {
      if (input.length === 0) {
        toast.error("Please provide an input");
        return;
      }
      setLoading(true);
      setTimeout(() => {
        setLoading(false);
        setFeatures(featuresData);
        localStorage.setItem("features", JSON.stringify(featuresData));
      }, 2000);
    }
  };

  const handleUrlEnter = (e) => {
    if (e.key === "Enter") {
      if (input.length === 0) {
        toast.error("Please provide an input");
        return;
      }
      if (!isUrlValid(input)) {
        toast.error("Please provide a valid URL");
        return;
      }
      setLoading(true);
      setTimeout(() => {
        setLoading(false);
        setFeatures(featuresData);
        localStorage.setItem("features", JSON.stringify(featuresData));
      }, 2000);
    }
  };

  const indexOfLastFeature = currentPage * featuresPerPage;
  const indexOfFirstFeature = indexOfLastFeature - featuresPerPage;
  const currentFeatures = features.slice(
    indexOfFirstFeature,
    indexOfLastFeature
  );

  const totalPages = Math.ceil(features.length / featuresPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const urlPattern = new RegExp(
    "^(https?:\\/\\/)?([\\w\\-]+\\.)+[\\w]{2,6}(\\/\\w*)?$"
  );

  const isUrlValid = (url) => urlPattern.test(url);

  const startIndex = (currentPage - 1) * featuresPerPage + 1;
  const endIndex = Math.min(currentPage * featuresPerPage, features.length);

  return (
    <div className="main">
      <FindFeaturesNavbar />
      <h1 className="find-features-heading">Find Features</h1>
      <div className="choose-feature-type">
        <p className="feature-type">Choose Feature Type:</p>
        <ReactSVG src={info} className="info-btn" />
        <input
          type="radio"
          id="url"
          name="feature-type"
          className="type-radio"
          value="url"
          onChange={handleSelection}
        />
        <label htmlFor="url" className="custom-radio"></label>
        <label htmlFor="url" className="type-label">
          URL
        </label>
        <input
          type="radio"
          id="dom"
          name="feature-type"
          className="type-radio"
          value="dom"
          onChange={handleSelection}
        />
        <label htmlFor="dom" className="custom-radio"></label>
        <label htmlFor="dom" className="type-label">
          DOM Structure
        </label>
      </div>
      {isSelected === "url" && (
        <div className="enter-details">
          <p className="enter-para">
            Enter the URL to find features<span className="mandatory">*</span>
          </p>
          <textarea
            className="textarea"
            onKeyDown={handleUrlEnter}
            onChange={(e) => setInput(e.target.value.trim())}
          />
        </div>
      )}
      {isSelected === "dom" && (
        <div className="enter-details">
          <p className="enter-para">
            Enter the DOM structure to find features
            <span className="mandatory">*</span>
          </p>
          <textarea
            className="textarea"
            onKeyDown={handleEnterPress}
            onChange={(e) => setInput(e.target.value.trim())}
          />
        </div>
      )}
      <div className="features-loader">
        {loading && input.length > 1 && (
          <>
            <Box sx={{ display: "flex", alignItems: "center", height: "100%" }}>
              <CircularProgress />
              <p style={{ marginLeft: "1%" }}>Loading features...</p>
            </Box>
            <div className="feature-cards">
              {[...Array(featuresPerPage)].map((_, index) => (
                <Skeleton
                  key={index}
                  sx={{
                    height: 126,
                    width: 344.2896,
                    marginTop: 3,
                    borderRadius: 0.5,
                    marginLeft: index % 3 === 0 ? 0 : 4,
                  }}
                  animation="wave"
                  variant="rectangular"
                />
              ))}
            </div>
          </>
        )}
        {!loading && features.length > 0 && (
          <>
            <div className="feature-count-display">
              <h3 className="feature-count-heading">Features</h3>
              <div className="feature-count">{features.length}</div>
            </div>
            <div className="feature-cards">
              {currentFeatures.map((feature, index) => (
                <div
                  key={index}
                  className="feature-card"
                  style={{ marginLeft: index % 3 === 0 ? 0 : 9 }}
                >
                  <h3>{feature.heading}</h3>
                  <p>{feature.paragraph}</p>
                </div>
              ))}
            </div>
            <div className="pagination">
              <p className="pagination-fix">
                Showing{" "}
                <b>
                  {startIndex}-{endIndex}
                </b>{" "}
                of <b>{features.length}</b>
              </p>
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            </div>
          </>
        )}
      </div>
      <ToastContainer />
    </div>
  );
}
