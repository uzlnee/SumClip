import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate, Link } from "react-router-dom";
import './App.css'
import GetVideo from "./get_video";
import Moreinfo from './more_info';

function MainPage() {
  const [inputValue, setInputValue] = useState("");
  const navigate = useNavigate();

  const handleSummarize = () => {
    if (inputValue.trim()) {
      navigate(`/summarize?url=${encodeURIComponent(inputValue)}`);
    } else {
      alert("Youtube 영상 링크를 입력해주세요!");
    }
  };

  return (
    <div className="container">
      <Link to="/" className="title">
        SUMCLIP
      </Link>
      <div className="main_div">
        <p className='description'>바쁘디바쁜 현대사회를 살아가고 있는 현대인들의 시간을 아끼기 위한 영상 요약 써-비스</p>
        <input 
          type="text"
          className="search-url"
          placeholder="Youtube 영상 링크를 입력하세요."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button onClick={handleSummarize}>요약하기</button>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/summarize" element={<GetVideo />} />
        <Route path="/more" element={<Moreinfo />} />
      </Routes>
    </Router>
  );
}

export default App
