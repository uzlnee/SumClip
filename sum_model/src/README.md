## 사용법

```
# 터미널 상에서의 명령어입니다.
# 1.
python3 video2audio.py # 실행 시 URL이 뜨라고 나옴. 여기에 유튜브 URL 입력
# video 폴더에 frames, audio.mp3, [유튜브 동영상 제목].mp4파일이 생성

# 2.
python3 audio2text.py # 실행 시
# video 폴더에 audio.wav, all_text.txt(전체 audio를 text로 변환한 txt파일),
# segments.csv(시간대별로 대사가 매핑 된 파일)이 생성됨

# 3.
# 환경 변수로 OPENAI_API_KEY를 설정 (연락주시면 드립니다 - 용준)

# 4.
python3 summarize.py # 실행 시 일단은 터미널상에서 Response를 확인할 수 있음.
# 아직은 audio에 대한 text만 모아 요약하였음.
# 출력 형식은 프롬프팅에 따라 바꿀 수 있음.

```

## 백 / 프론트 사용법

```
# 2개의 터미널 켜서
# 1. 첫번째 터미널은 frontend 쪽으로 이동 후 npm run dev 실행 (실행 전 node.js 설치 필수, pip로 말고 프로그램 자체를)
# 2. backend 실행 전 pip install fastapi uvicorn pydantic pydantic_settings 로 설치 환경 구축
# 3. 두번째 터미널은 backend 쪽으로 이동 후 uvicorn app.main:app --reload --port 8000으로 실행
```

## 감정 분석 데이터 가져오기

`comment_analyzer`의 `get_sentiment_df` 함수를 사용하여 YouTube 댓글 감정 분석 결과를 DataFrame으로 받아올 수 있습니다.

```python
# 함수 import
from comment_analyzer import get_sentiment_df

# 사용 예시
video_url = "https://www.youtube.com/watch?v=example"
df = get_sentiment_df(video_url)
```

### 반환되는 DataFrame 구조

- text: 댓글 내용
- likes: 좋아요 수
- author: 작성자
- published_at: 작성 시간
- sentiment: 감정 분석 결과 ('긍정', '부정', '중립')

## 참고용 Response

![poster](./screenshot/스크린샷%202024-12-19%20오전%2012.47.16.png)
