import re
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import networkx as nx

import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords


# Kiwi 형태소 분석기 초기화
kiwi = Kiwi()

def extract_nouns_from_text(file_path):
    """
    주어진 텍스트 파일에서 명사만 추출하여 반환하는 함수
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 텍스트에서 문장 단위로 나누기
    sentences = text.split('\n')

    # 명사 추출
    nouns = []
    for sentence in sentences:
        result = kiwi.analyze(sentence)
        for item in result:
            for morpheme in item[0]:
                if morpheme[1] == 'NNG' or morpheme[1] == 'NNP':  # 일반 명사(NNG), 고유 명사(NNP)
                    nouns.append(morpheme[0])

    return nouns

def create_cooccurrence_matrix(nouns, window_size=2):
    """
    명사 리스트에서 단어 간 공동 출현 행렬을 생성하는 함수
    - window_size: 근접 단어를 고려할 범위
    """
    cooccurrence = Counter()
    
    # 문장에서 단어들이 등장하는 간격을 기반으로 공동 출현 빈도 계산
    for i in range(len(nouns) - window_size + 1):
        for j in range(i+1, min(i + window_size, len(nouns))):
            cooccurrence[(nouns[i], nouns[j])] += 1
            cooccurrence[(nouns[j], nouns[i])] += 1  # 양방향 관계
    return cooccurrence

def generate_wordcloud(nouns):
    """
    명사 리스트를 기반으로 워드클라우드를 생성하는 함수
    """
    word_freq = Counter(nouns)

    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path="/Users/jeong-yujin/Desktop/SumClip/src/sumclipenv/lib/python3.11/site-packages/koreanize_matplotlib/fonts/NanumGothic.ttf",
        background_color="white",
        width=480,
        height=480,
        max_words=100,
        # colormap="Blues"
    ).generate_from_frequencies(word_freq)

    # 워드클라우드 시각화
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def generate_sankey_diagram(cooccurrence):
    """
    명사 리스트를 기반으로 Sankey Diagram을 생성하는 함수
    """
    # 관계가 잘 형성된 데이터 (빈도가 높은 관계 추출)
    threshold = 2  # 공동 출현 빈도가 일정 수준 이상일 때만 관계로 채택
    relations = [(k[0], k[1], v) for k, v in cooccurrence.items() if v >= threshold]

    # Sankey Diagram을 위한 노드, 엣지 정의
    labels = list(set([noun for relation in relations for noun in relation[:2]]))
    label_map = {label: index for index, label in enumerate(labels)}

    # 엣지의 인덱스를 정의 (각각의 관계를 나타내기 위해)
    source = [label_map[relation[0]] for relation in relations]
    target = [label_map[relation[1]] for relation in relations]
    value = [relation[2] for relation in relations]  # 공동 출현 빈도

    # Sankey Diagram 시각화
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    ))

    fig.update_layout(title="Sankey Diagram", font_size=10)
    fig.show()

def generate_barplot(nouns):
    """
    명사 리스트에서 상위 20개의 단어 빈도를 기반으로 가로 바 플롯을 생성하는 함수
    """
    # 빈도수 계산
    word_freq = Counter(nouns)

    # 빈도수가 높은 상위 20개 단어 추출
    top_words = word_freq.most_common(20)
    words, freqs = zip(*top_words)

    # 색상 지정
    colors = sns.color_palette('copper', 20)

    # 바 플롯 시각화 (내림차순)
    plt.figure(figsize=(10, 8))
    plt.barh(words, freqs, color=colors)
    plt.xlabel('빈도수')
    plt.title('Top 20 명사 빈도수 (내림차순)')
    plt.gca().invert_yaxis()  # 내림차순으로 정렬
    plt.show()

def main(file_path):
    # 텍스트에서 명사 추출
    nouns = extract_nouns_from_text(file_path)

    # 워드클라우드 생성
    generate_wordcloud(nouns)

    # 공동 출현 행렬 생성
    cooccurrence = create_cooccurrence_matrix(nouns)

    # Sankey Diagram 생성
    generate_sankey_diagram(cooccurrence)

    # 상위 20개 명사 빈도수 바 플롯 생성
    generate_barplot(nouns)

