import os

import openai
import pandas as pd
from dotenv import load_dotenv


class summarizer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(backend_dir, ".env")

        load_dotenv(env_path)
        
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)

    def generate(self, text):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 동영상의 Script를 읽고 요약문을 작성하는 Agent입니다. 주어지는 text를 읽고 동영상의 내용을 500자 이내로 요약하세요.
                                출력 형식은
                                [간단 요약]
                                [핵심 내용]
                                [중요 포인트]
                                입니다.""",
                },
                {
                    "role": "user",
                    "content": f"""{text}
                                """,
                },
            ],
        )
        response = response.choices[0].message.content.strip()
        return response


if __name__ == "__main__":
    basepath = "./video/"
    df = pd.read_csv(basepath + "segments.csv")

    with open(basepath + "all_text.txt", "r", encoding="utf-8") as f:
        text = f.readline()

    # 환경 변수에서 API 키 불러오기
    model = summarizer()
    response = model.generate(text)
    print(response)
