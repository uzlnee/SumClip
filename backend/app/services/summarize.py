import os

import openai
import pandas as pd


class summarizer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)

    def generate(self, text, query):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": query,
                },
                {
                    "role": "user",
                    "content": f"""{text}
                                """,
                },
            ],
        )
        response = response.choices[0].message.content.strip()
        simple = response.find('[간단 요약]')
        core = response.find('[핵심 내용]')
        point = response.find('[중요 포인트]')
        simple = response[:core] if simple != -1 else '[간단 요약] 없음'
        core = response[core:point] if core != -1 else '[핵심 내용] 없음'
        point = response[point:] if point != -1 else '[중요 포인트] 없음'
        
        return simple, core, point


if __name__ == "__main__":
    basepath = "./video/"
    df = pd.read_csv(basepath + "segments.csv")
    # txt파일의 경로를 바탕으로 요약합니다.
    with open(basepath + "all_text_refined.txt", "r", encoding="utf-8") as f:
        text = f.readline()

    # 환경 변수에서 API 키 불러오기
    model = summarizer()
    query = """당신은 동영상의 Script를 읽고 요약문을 작성하는 Agent입니다. 주어지는 text를 읽고 동영상의 내용을 500자 이내로 요약하세요.
                                출력 형식은
                                [간단 요약]
                                [핵심 내용]
                                [중요 포인트]
                                입니다."""
    simple, core, point = model.generate(text, query)
    print(simple)
    print(core)
    print(point)
