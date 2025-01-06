import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./more_info.css";

const Moreinfo = () => {
  const [activeTab, setActiveTab] = useState("간단 요약");
  const [activeMenuItem, setActiveMenuItem] = useState("Summary");
  const [showTab, setShowTab] = useState(true);
  const [wordCloudImg, setWordCloudImg] = useState(null);
  const [simpleText, setSimpleText] = useState("");
  const [coreText, setCoreText] = useState("");
  const [pointText, setPointText] = useState("");
  const [treeImg, setTreeImg] = useState(null);
  const [responseImg, setResponseImg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const BACKEND_URL = "http://localhost:8000";

  const handleTabClick = (tabName) => {
    setActiveTab(tabName);
  };

  const handleMenuItemClick = (menuItemName) => {
    setActiveMenuItem(menuItemName);
    if (menuItemName === "Summary") {
        setActiveTab("간단 요약");
        setShowTab(true);
      } else if (menuItemName === "Infographic") {
        setActiveTab("키워드 클라우드");
        setShowTab(true);
      } else if (menuItemName === "Response") {
        setShowTab(false);
      }

  };
  
  const getTabs = () => {
    switch (activeMenuItem) {
      case "Infographic":
        return ["키워드 클라우드", "트리맵"];
      case "Summary":
        return ["간단 요약", "핵심 내용", "중요 포인트"];
      default:
        return []
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        let response;
        if (activeMenuItem === "Response") {
          response = await fetch(`${BACKEND_URL}/more/sentiment`);
        } else {
          const endpoints = {
            "간단 요약": "/summary/simple",
            "핵심 내용": "/summary/core",
            "중요 포인트": "/summary/point",
            "키워드 클라우드": "/more/wordcloud",
            "트리맵": "/more/tree",
          };
          response = await fetch(`${BACKEND_URL}${endpoints[activeTab]}`);
        }

        if (!response.ok) throw new Error(`Failed to fetch ${activeTab}`);

        if (activeTab === "키워드 클라우드" || activeTab === "트리맵" || activeMenuItem === "Response") {
          const blob = await response.blob();
          if (activeTab === "키워드 클라우드") setWordCloudImg(blob);
          else if (activeTab === "트리맵") setTreeImg(blob);
          else if (activeMenuItem === "Response") setResponseImg(blob);
        } else {
          const text = await response.text();
          if (activeTab === "간단 요약") setSimpleText(text);
          else if (activeTab === "핵심 내용") setCoreText(text);
          else if (activeTab === "중요 포인트") setPointText(text);
        }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [activeTab, activeMenuItem]);

  const renderImageFromBlob = (blob) => {
    if (!blob) return null;
    const url = URL.createObjectURL(blob);
    useEffect(() => {
      return () => URL.revokeObjectURL(url);
    }, [blob]);
    return (
      <img
        src={url}
        alt="Rendered"
        style={{
          maxWidth: "100%",
          maxHeight: "100%",
          display: "block",
          margin: "0 auto",
        }}
      />
    );
  };

  return (
    <div className="container">
      <Link to="/" className="title">
        SUMCLIP
      </Link>
      <div className="tabs">
        {getTabs().map((tabName) => (
          <div
            key={tabName}
            className={`tab ${activeTab === tabName ? "active" : ""}`}
            onClick={() => handleTabClick(tabName)}
          >
            {tabName}
          </div>
        ))}
      </div>
      <div 
        className="content"
        style={{
          marginTop: activeMenuItem === "Response" ? "41px" : "0px",
        }}
      >
        <div className="menu">
          {["Summary", "Infographic", "Response"].map((menuItemName) => (
            <div
              key={menuItemName}
              className={`menu-item ${
                activeMenuItem === menuItemName ? "selected" : ""
              }`}
              onClick={() => handleMenuItemClick(menuItemName)}
            >
              {menuItemName}
            </div>
          ))}
        </div>
        <div className="content-area">
          {loading && <div className="loading">Loading...</div>}
          {error && <div className="error">{error}</div>}
          {activeTab === "간단 요약" && !loading && !error && (
            <div className="simple-text">{simpleText}</div>
            
          )}
          {activeTab === "핵심 내용" && !loading && !error && (
            <div className="core-text">{coreText}</div>
          )}
          {activeTab === "중요 포인트" && !loading && !error && (
            <div className="point-text">{pointText}</div>
          )}
          {activeTab === "키워드 클라우드" && renderImageFromBlob(wordCloudImg)}
          {activeTab === "트리맵" && renderImageFromBlob(treeImg)}
          {activeMenuItem === "Response" && renderImageFromBlob(responseImg)}
        </div>
      </div>
    </div>
  );
};

export default Moreinfo;
