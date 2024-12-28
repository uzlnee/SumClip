import React, { useState } from "react";
import "./more_info.css";

const Moreinfo = () => {
  const [activeTab, setActiveTab] = useState("전체 요약");
  const [activeMenuItem, setActiveMenuItem] = useState("Summary");
  const [wordCloudUrl, setWordCloudUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTabClick = (tabName) => {
    setActiveTab(tabName);
  };

  const handleMenuItemClick = (menuItemName) => {
    setActiveMenuItem(menuItemName);
    if (menuItemName === "Summary") {
        setActiveTab("전체 요약");
      } else if (menuItemName === "Infographic") {
        setActiveTab("키워드 클라우드");
      } else if (menuItemName === "Response") {
        setActiveTab("Positive");
      }
  };
  
  const getTabs = () => {
    switch (activeMenuItem) {
      case "Infographic":
        return ["키워드 클라우드", "마인드맵"];
      case "Response":
        return ["Positive", "Negative"];
      default:
        return ["전체 요약", "타임스탬프", "간단 요약"];
    }
  };

  // useEffect(() => {
  //   if (activeTab === "키워드 클라우드") {
  //     fetch("http://localhost:5000/wordcloud") // 백엔드 API 호출
  //       .then((response) => {
  //         if (response.ok) {
  //           return response.blob();
  //         }
  //         throw new Error("Failed to fetch wordcloud");
  //       })
  //       .then((blob) => {
  //         setWordCloudUrl(URL.createObjectURL(blob)); // 이미지 URL 생성
  //       })
  //       .catch((error) => console.error(error));
  //   }
  // }, [activeTab]);
  
  // useEffect(() => {
  //   if (activeTab === "Positive") {
  //     setLoading(true);
  //     setError(null);

  //     fetch("http://localhost:5000/analyze_comments", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify({ video_url: "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" }),
  //     })
  //       .then((response) => {
  //         if (!response.ok) {
  //           throw new Error("Failed to fetch comments");
  //         }
  //         return response.json();
  //       })
  //       .then((data) => {
  //         setPositiveComments(data); // 데이터 저장
  //       })
  //       .catch((err) => {
  //         setError(err.message);
  //       })
  //       .finally(() => {
  //         setLoading(false);
  //       });
  //   }
  // }, [activeTab]);

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
      <div className="content">
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
          {/* {activeTab === "키워드 클라우드" && wordCloudUrl && (
            <img
              src={wordCloudUrl}
              alt="Word Cloud"
              className="wordcloud-image"
            />
          )}
          {activeTab === "Positive" && (
            <>
              {loading ? (
                <p>Loading comments...</p>
              ) : error ? (
                <p>Error: {error}</p>
              ) : positiveComments.length > 0 ? (
                <ul>
                  {positiveComments.map((comment, index) => (
                    <li key={index}>
                      <p><strong>{comment.author}</strong>:</p>
                      <p>{comment.text}</p>
                      <p>Likes: {comment.likes}</p>
                      <p>Published: {new Date(comment.published_at).toLocaleString()}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No positive comments found.</p>
              )}
            </>
          )} */}
        </div>
      </div>
    </div>
  );
};

export default Moreinfo;
