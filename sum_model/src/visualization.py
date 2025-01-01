import re
from collections import Counter, defaultdict

import koreanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

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


def create_cooccurrence_matrix(nouns, window_size=2):
    """
    명사 리스트에서 단어 간 공동 출현 행렬을 생성하는 함수
    - window_size: 근접 단어를 고려할 범위
    """
    cooccurrence = Counter()

    # 문장에서 단어들이 등장하는 간격을 기반으로 공동 출현 빈도 계산
    for i in range(len(nouns) - window_size + 1):
        for j in range(i + 1, min(i + window_size, len(nouns))):
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
        font_path="/Users/jeong-yujin/Desktop/SumClip/sum_model/src/fonts/NanumGothicBold.ttf",
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


def build_tree_structure(sentences, n_clusters=5):
    """
    문장에서 TF-IDF와 K-Means를 사용해 클러스터링 후 계층 구조 생성
    - sentences: 문장 리스트
    """
    # 1. TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    
    # 2. K-Means 클러스터링
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)  # 문서별 클러스터 할당
    
    # 3. 클러스터별 키워드 추출
    terms = vectorizer.get_feature_names_out()
    cluster_keywords = defaultdict(list)
    for idx, label in enumerate(labels):
        feature_indices = X[idx].nonzero()[1]
        keywords = [terms[i] for i in feature_indices]
        cluster_keywords[f"Cluster {label+1}"].extend(keywords)
    
    # 4. 트리 데이터 구조 생성
    tree_data = {"name": "Root", "children": []}
    for cluster, keywords in cluster_keywords.items():
        tree_data["children"].append({
            "name": cluster,
            "children": [{"name": keyword} for keyword in keywords[:10]]  # 상위 10개 키워드만 포함
        })
    
    return tree_data

def build_plotly_tree(tree_data, parent=""):
    """
    Plotly 트리 다이어그램을 위한 데이터 생성
    - 트리 데이터를 재귀적으로 탐색하여 labels, parents 리스트 생성
    """
    labels = []
    parents = []
    labels.append(tree_data["name"])
    parents.append(parent)
    for child in tree_data.get("children", []):
        child_labels, child_parents = build_plotly_tree(child, tree_data["name"])
        labels.extend(child_labels)
        parents.extend(child_parents)
    return labels, parents

def visualize_tree_diagram(tree_data):
    """
    트리 계층 구조를 Plotly로 시각화하는 함수
    """
    labels, parents = build_plotly_tree(tree_data)

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        branchvalues="total"
    ))

    fig.update_layout(
        title="트리 다이어그램",
        margin=dict(t=50, l=25, r=25, b=25)
    )

    fig.show()

def generate_treemap(nouns):
    word_freq = Counter(nouns)
    top_words = word_freq.most_common(20)
    words, freqs = zip(*top_words)
    fig = px.treemap(
        names=words, parents=[""] * len(words), values=freqs, title="트리맵"
    )
    fig.show()


def main(file_path):
    # 텍스트에서 명사 추출
    nouns = extract_nouns_from_text(file_path)
    flat_nouns = [word for sublist in nouns for word in sublist]

    # 워드클라우드 생성
    generate_wordcloud(flat_nouns)

    # 공동 출현 행렬 생성
    cooccurrence = create_cooccurrence_matrix(flat_nouns)


    # 트리 계층 구조 생성
    tree_structure = build_tree_structure(flat_nouns, n_clusters=5)

    # 트리 다이어그램 시각화
    visualize_tree_diagram(tree_structure)

    generate_treemap(flat_nouns)
