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

## 참고용 Response

![poster](./screenshot/스크린샷%202024-12-19%20오전%2012.47.16.png)