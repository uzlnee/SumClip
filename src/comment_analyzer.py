import os
from urllib.parse import parse_qs, urlparse

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from openai import OpenAI

load_dotenv()


def get_video_id(url):
    """YouTube URL에서 비디오 ID를 추출하는 함수"""
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query)["v"][0]
    return None


def get_comments(youtube, video_id, max_results=10):
    """YouTube 동영상의 인기 댓글을 가져오는 함수"""
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results,
            order="relevance",  # 인기 댓글 순으로 정렬
        )

        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append(
                {
                    "text": comment["textDisplay"],
                    "likes": comment["likeCount"],
                    "author": comment["authorDisplayName"],
                    "published_at": comment["publishedAt"],
                }
            )

    except Exception as e:
        print(f"댓글 불러오기 중 오류 발생: {str(e)}")

    return comments


def analyze_sentiment(client, text):
    """OpenAI API를 사용하여 텍스트의 감정을 분석하는 함수"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "다음 댓글의 감정을 분석하세요. '긍정', '부정', '중립' 중 하나로만 답변하세요.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        sentiment = response.choices[0].message.content.strip()
        return sentiment

    except Exception as e:
        print(f"감정 분석 중 오류 발생: {str(e)}")
        return "분석 실패"


def main():
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not youtube_api_key or not openai_api_key:
        print("Error: API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        return

    # API 클라이언트 초기화
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    openai_client = OpenAI(api_key=openai_api_key)

    video_url = input("분석할 YouTube 영상의 URL을 입력하세요: ")
    video_id = get_video_id(video_url)

    if not video_id:
        print("올바른 YouTube URL이 아닙니다.")
        return

    # 댓글 가져오기
    print("인기 댓글을 가져오는 중...")
    comments = get_comments(youtube, video_id)

    if not comments:
        print("댓글을 가져올 수 없습니다.")
        return

    df = pd.DataFrame(comments)

    # 좋아요 수로 정렬
    df = df.sort_values("likes", ascending=False)

    print("댓글 감정 분석 중...")
    df["sentiment"] = df["text"].apply(lambda x: analyze_sentiment(openai_client, x))

    print("\n=== 인기 댓글 감정 분석 결과 ===")
    for idx, row in df.iterrows():
        print(f"\n{idx+1}번째 댓글:")
        print(f"작성자: {row['author']}")
        print(
            f"내용: {row['text'][:100]}..."
            if len(row["text"]) > 100
            else f"내용: {row['text']}"
        )
        print(f"좋아요 수: {row['likes']}")
        print(f"감정 분석: {row['sentiment']}")

    # 감정 분석 통계
    sentiment_stats = df["sentiment"].value_counts()
    print("\n=== 감정 분석 통계 ===")
    print(sentiment_stats)


if __name__ == "__main__":
    main()
