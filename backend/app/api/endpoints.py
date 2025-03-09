from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.video2audio import process_youtube_video
from app.services.audio2text import AudioTranslator, process_audio_from_videos
from app.services.summarize import summarizer
from app.services.TextViz import generate_wordcloud, extract_nouns_from_text, generate_treemap_with_squarify
from app.services.comment_analyzer import visualize_sentiment_analysis, get_sentiment_df
from app.models import schemas
from app.core.database import get_db
from app.models.models import Video, Analysis
import sys
import os
import openai
import base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_environment():
    required_vars = ["OPENAI_API_KEY", "DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"필수 환경 변수가 없습니다: {','.join(missing_vars)}")
    
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv(os.path.join(BASE_DIR, ".env"))

verify_environment()

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

@router.get("/summarize")
async def get_summary(url: str, db:Session = Depends(get_db)):
    try:
        logger.info(f"Processing URL: {url}")

        backend_dir = os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        video_dir = os.path.normpath(os.path.join(backend_dir, "video"))

        os.makedirs(video_dir, exist_ok=True)

        audio_file_path = await process_youtube_video(url)
        print(f"Video processed successfully: {audio_file_path}")

        audio_path = os.path.normpath(os.path.join(backend_dir, audio_file_path))
        print(f"Using audio path: {audio_path}")

        if not os.path.exists(audio_path):
            print(f"File not found at: {audio_path}")
            print(f"Directory contents: {os.listdir(os.path.dirname(audio_path))}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        await process_audio_from_videos([audio_path])
        print("Audio translated successfully")

        text_path = os.path.normpath(os.path.join(video_dir, "all_text.txt"))
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.readline()

        model = summarizer()
        query = """당신은 동영상의 Script를 읽고 요약문을 작성하는 Agent입니다. 주어지는 text를 읽고 동영상의 내용을 500자 이내로 요약하세요.
                                출력 형식은
                                [간단 요약]
                                [핵심 내용]
                                [중요 포인트]
                                입니다."""
        simple, core, point = await model.generate(text, query)

        video = Video(
            youtube_link=url,
            simple_summary=simple,
            core_summary=core,
            point_summary=point
        )
        db.add(video)
        db.commit()
        db.refresh(video)

        text_path = os.path.normpath(os.path.join(video_dir, "all_text.txt"))
        nouns = extract_nouns_from_text(text_path)
        sentiment_df = get_sentiment_df(url)

        visualizations = {
            'wordcloud': generate_wordcloud(nouns),
            'tree': generate_treemap_with_squarify(nouns),
            'sentiment': visualize_sentiment_analysis(sentiment_df),
        }

        for viz_type, image_data in visualizations.items():
            if not image_data:
                logger.warning(f"No image data generated for {viz_type}")
                continue

            analysis = Analysis(
                video_id=video.id,
                analysis_type=viz_type,
                image_data=image_data,
                image_format='png'
            )
            db.add(analysis)

        db.commit()

        print("Summary and visualizations generated successfully")

        return {"simple": simple, "core": core, "point": point, "video_id": video.id}
    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Error details: {str(e)}")
        print(f"Video directory exists: {os.path.exists(video_dir)}")
        if os.path.exists(video_dir):
            print(f"Video directory contents: {os.listdir(video_dir)}")
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )

@router.get("/more/{analysis_type}")
async def get_analysis(analysis_type: str, db:Session = Depends(get_db)):
    valid_types = ["wordcloud", "sentiment", "treemap"]
    if analysis_type not in valid_types:
        raise HTTPException(status_code=400, detail="유효하지 않은 분석 타입")
    
    try:
        analysis = db.query(Analysis)\
            .filter(Analysis.analysis_type == analysis_type)\
            .order_by(Analysis.video_id.desc())\
            .first()
    
        if not analysis:
            raise HTTPException(status_code=404, detail=f"{analysis_type}를 찾을 수 없음")
        
        image_base64 = base64.b64encode(analysis.image_data).decode('utf-8')

        return {
            "image_data": f"data:image/{analysis.image_format};base64, {image_base64}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/more/summary/{summary_type}")
async def get_summary_by_type(summary_type:str, db: Session = Depends(get_db)):
    try:
        if summary_type not in ["simple", "core", "point"]:
            raise HTTPException(status_code=400, detail="Unvalid summary type")
        
        video = db.query(Video)\
            .order_by(Video.id.desc())\
            .first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Cannot find summary information")
        
        summary_field = f"{summary_type}_summary"

        if not hasattr(video, summary_field):
            raise HTTPException(status_code=404, detail=f"{summary_type} type is not found")
        
        return {
            "summary": getattr(video, summary_field)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))