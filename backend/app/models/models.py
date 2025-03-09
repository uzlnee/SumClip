from sqlalchemy import Column, Integer, String, LargeBinary, Text, DateTime, ForeignKey, Enum\
                        ,Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    youtube_link = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, index=True)
    simple_summary = Column(Text)
    core_summary = Column(Text)
    point_summary = Column(Text)
    # summary = Column(Text)
    analysis = relationship("Analysis", back_populates="video")

class AnalysisType(str, Enum):
    WORDCLOUD="wordcloud"
    SENTIMENT = "sentiment"
    TREE = "tree"
    
class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    image_format = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, index=True)
    video = relationship("Video", back_populates="analysis")
    
Index('idx_video_analysis', Analysis.video_id, Analysis.analysis_type)