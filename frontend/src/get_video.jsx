import React, { useState, useEffect } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import './get_video.css'

function GetVideo() {
  const location = useLocation();
  const navigate = useNavigate();
  const [videoTitle, setVideoTitle] = useState(""); // 영상 제목 상태
  const [simpleSummary, setSimpleSummary] = useState("");
  const [coreSummary, setCoreSummary] = useState("");
  const [pointSummary, setPointSummary] = useState("");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  const API_KEY = "AIzaSyCI9AppENCFt1tU9iTkYbl83OTW27E1P2k";
  const BACKEND_URL = "http://localhost:8000";
  // URL에서 query parameter를 가져오는 함수
  const getQueryParam = (param) => {
    const queryParams = new URLSearchParams(location.search);
    return queryParams.get(param);
  };

  const videoUrl = getQueryParam("url"); // 넘어온 input 값 (url)
  let videoId = null;

  if (videoUrl) {
    const urlParams = new URLSearchParams(new URL(videoUrl).search);
    videoId = urlParams.get("v"); // 'v'에 해당하는 영상 ID 가져오기
  }

  const thumbnailUrl = videoId
    ? `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`
    : null;

  const fetchVideoTitle = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&key=${API_KEY}&part=snippet`
      );

      if (!response.ok) throw new Error("Failed to fetch video data");

      const data = await response.json();

      // 영상 제목 설정
      if (data.items.length > 0) {
        setVideoTitle(data.items[0].snippet.title);
      } else {
        throw new Error("No video data found");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const processVideo = async () => {
    if (!videoUrl) return;

    try {
      setProcessing(true);
      setError(null);

      const response = await fetch(
        `${BACKEND_URL}/summarize?url=${encodeURIComponent(videoUrl)}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) throw new Error("Failed to process the video");

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setSimpleSummary(data.simple);
    } catch (err) {
      setError(err.message);
    } finally {
      setProcessing(false);
    }
  };

  useEffect(() => {
    if (videoId) {
      fetchVideoTitle();
      processVideo();
    }
  }, [videoId]);

  return (
    <div className="container">
      <Link to="/" className="title">
        SUMCLIP
      </Link>
      <div className="video-card">
        <div className="video-card-header">
          <div className="action-container" onClick={() => navigate("/")}>
            <img src="src\image2.png" alt="처음으로" className="action-image" />
            <span className="action-text">처음으로</span>
          </div>
          {thumbnailUrl && (
            <img
              src={thumbnailUrl}
              alt="YouTube Thumbnail"
              className="youtube-thumbnail"
            />
          )}
          <div className="action-container" onClick={() => navigate("/more")}>
            <img src="src\image3.png" alt="자세히 보러가기" className="action-image" />
            <span className="action-text">자세히 보러가기</span>
          </div>
        </div>
        <p className="video-title">{videoTitle}</p>
        {loading ? (
            <p className="loading">로딩 중...</p>
          ) : error ? (
            <p className="error">에러 발생: {error}</p>
          ) : (
            <>
              <div className="video-summary">
                <p><strong>간단 요약:</strong> {simpleSummary}</p>
            </div>
            </>
          )}
      </div>
    </div>
  );
}

export default GetVideo;
