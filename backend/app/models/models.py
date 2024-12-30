from sqlalchemy import Column, Integer, String, LargeBinary, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    youtube_link = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    simple_summary = Column(Text)
    core_summary = Column(Text)
    point_summary = Column(Text)
    # summary = Column(Text)
    analysis = relationship("Analysis", back_populates="video")
    
class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    analysis_type = Column(String)
    image_data = Column(LargeBinary)
    image_format = Column(String)
    video = relationship("Video", back_populates="analysis")