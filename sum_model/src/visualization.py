import re
import numpy as np
from collections import Counter, defaultdict

import koreanize_matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from wordcloud import WordCloud


# Kiwi 형태소 분석기 초기화
kiwi = Kiwi()


def extract_nouns_from_text(file_path):
    """
    주어진 텍스트 파일에서 명사만 추출하여 반환하는 함수
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # 텍스트에서 문장 단위로 나누기
    sentences = text.split("\n")

    # 명사 추출
    nouns = []
    for sentence in sentences:
        result = kiwi.analyze(sentence)
        for item in result:
            for morpheme in item[0]:
                if morpheme[1] in {"NNG", "NNP"}:  # 일반 명사(NNG), 고유 명사(NNP)
                    nouns.append(morpheme[0])

    return nouns, sentences


def generate_wordcloud(nouns):
    """
    명사 리스트를 기반으로 워드클라우드를 생성하는 함수
    """
    word_freq = Counter(nouns)

    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path="/Users/jeong-yujin/Desktop/SumClip/sum_model/src/sumclipenv/lib/python3.11/site-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf",
        background_color="white",
        width=480,
        height=480,
        max_words=100,
        # colormap="Blues"
    ).generate_from_frequencies(word_freq)

    # 워드클라우드 시각화
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def generate_treemap_with_squarify(nouns):
    """
    Squarify를 사용하여 트리맵을 생성하고 텍스트를 가운데 정렬하는 함수
    """
    word_freq = Counter(nouns)
    top_words = word_freq.most_common(20)
    words, freqs = zip(*top_words)

    # Squarify의 값을 정규화
    normalized_sizes = squarify.normalize_sizes(freqs, 100, 100)
    rects = squarify.squarify(normalized_sizes, 0, 0, 100, 100)

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab20c(range(len(rects)))  # 색상 지정
    for i, rect in enumerate(rects):
        x, y, w, h = rect['x'], rect['y'], rect['dx'], rect['dy']
        ax.add_patch(plt.Rectangle((x, y), w, h, color=colors[i]))
        ax.text(
            x + w / 2, y + h / 2, words[i],
            ha="center", va="center", fontsize=13, color="black"
        )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()


def main(file_path):
    # 텍스트에서 명사 추출
    nouns = extract_nouns_from_text(file_path)
    flat_nouns = [word for sublist in nouns for word in sublist]

    # 워드클라우드 생성
    generate_wordcloud(flat_nouns)

    # Squarify 트리맵 생성
    generate_treemap_with_squarify(flat_nouns)
