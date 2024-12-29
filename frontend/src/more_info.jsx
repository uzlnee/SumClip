import React, { useState } from "react";
import "./more_info.css";

const Moreinfo = () => {
  const [activeTab, setActiveTab] = useState("전체 요약");
  const [activeMenuItem, setActiveMenuItem] = useState("Summary");
  const [showTab, setShowTab] = useState(true);
  const [wordCloudImg, setWordCloudImg] = useState(null);
  const [simpleText, setSimpleText] = useState("");
  const [coreText, setCoreText] = useState("");
  const [pointText, setPointText] = useState("");
  const [treeImg, setTreeImg] = useState(null);
  const [barImg, setBarImg] = useState(null);
  const [sankeyImg, setSankeyImg] = useState(null);
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
        return ["키워드 클라우드", "트리", "막대", "SANKEY"];
      case "Summary":
        return ["간단 요약", "핵심 내용", "중요 포인트"];
      default:
        return []
    }
  };

  useEffect(() => {
    if (activeTab === "간단 요약") {
      setLoading(true);
      fetch(`${BACKEND_URL}/summary/simple`)
        .then((response) => {
          if (response.ok) {
            return response.text();
          }
          throw new Error("Failed to fetch simple summary");
        })
        .then((text) => {
          setSimpleText(text);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "핵심 내용") {
      setLoading(true);
      fetch(`${BACKEND_URL}/summary/core`)
        .then((response) => {
          if (response.ok) {
            return response.text();
          }
          throw new Error("Failed to fetch core summary");
        })
        .then((text) => {
          setCoreText(text);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "중요 포인트트") {
      setLoading(true);
      fetch(`${BACKEND_URL}/summary/point`)
        .then((response) => {
          if (response.ok) {
            return response.text();
          }
          throw new Error("Failed to fetch point summary");
        })
        .then((text) => {
          setPointText(text);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "키워드 클라우드") {
      setLoading(true);
      fetch(`${BACKEND_URL}/more/wordcloud`)
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Failed to fetch wordcloud");
        })
        .then((blob) => {
          setWordCloudImg(blob);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
      });
    }
  }, [activeTab]);
  
  useEffect(() => {
    if (activeTab === "트리") {
      setLoading(true);
      fetch(`${BACKEND_URL}/more/tree`)
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Failed to fetch tree image");
        })
        .then((blob) => {
          setTreeImg(blob);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "막대") {
      setLoading(true);
      fetch(`${BACKEND_URL}/more/bar`)
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Failed to fetch bar image");
        })
        .then((blob) => {
          setBarImg(blob);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "SANKEY") {
      setLoading(true);
      fetch(`${BACKEND_URL}/more/sankey`)
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Failed to fetch sankey image");
        })
        .then((blob) => {
          setSankeyImg(blob);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeMenuItem === "response") {
      setLoading(true);
      fetch(`${BACKEND_URL}/more/sentiment`)
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Failed to fetch response image");
        })
        .then((blob) => {
          setResponseImg(blob);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setError(error.message);
          setLoading(false);
        });
    }
  }, [activeTab]);

  const renderImageFromBlob = (blob) => {
    if (!blob) return null;
    const url = URL.createObjectURL(blob); // Blob을 URL로 변환
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
        onLoad={() => URL.revokeObjectURL(url)} // 메모리 누수를 방지하기 위해 URL 해제
      />
    );
  };

  return (
    <div className="container">
      <h1 className="title">SUMCLIP</h1>
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
          {activeTab === "트리" && renderImageFromBlob(treeImg)}
          {activeTab === "막대" && renderImageFromBlob(barImg)}
          {activeTab === "SANKEY" && renderImageFromBlob(sankeyImg)}
          {activeMenuItem === "response" && renderImageFromBlob(responseImg)}
        </div>
      </div>
    </div>
  );
};

export default Moreinfo;
