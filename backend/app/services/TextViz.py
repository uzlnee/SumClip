import re
from collections import Counter, defaultdict

import koreanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import io
import base64
import os
from PIL import Image

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from wordcloud import WordCloud
import networkx as nx

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Kiwi 형태소 분석기 초기화
kiwi = Kiwi()

FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'statics', 'fonts', 'NANUMGOTHIC-REGULAR.TTF')

print(f"Font path: {FONT_PATH}")
print(f"Font exists: {os.path.exists(FONT_PATH)}")

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
                if (
                    morpheme[1] == "NNG" or morpheme[1] == "NNP"
                ):  # 일반 명사(NNG), 고유 명사(NNP)
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
        font_path=FONT_PATH,
        background_color="white",
        width=480,
        height=480,
        max_words=100,
        colormap="Blues"
    ).generate_from_frequencies(word_freq)

    img_buffer = io.BytesIO()

    # 워드클라우드 시각화
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()

    return img_buffer.getvalue()


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
    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels
            ),
            link=dict(source=source, target=target, value=value),
        )
    )

    # fig.update_layout(title="Sankey Diagram", font_size=10)
    # fig.show()

    img_bytes = fig.to_image(format="png")
    return img_bytes


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
    colors = sns.color_palette("copper", 20)

    img_buffer = io.BytesIO()
    # 바 플롯 시각화 (내림차순)
    plt.figure(figsize=(10, 8))
    plt.barh(words, freqs, color=colors)
    plt.xlabel("빈도수")
    plt.title("Top 20 명사 빈도수 (내림차순)")
    plt.gca().invert_yaxis()  # 내림차순으로 정렬
    # plt.show()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()

    return img_buffer.getvalue()

def build_tree_structure(nouns, n_clusters=5):
    """
    명사 리스트에서 트리 계층 구조 데이터를 생성하는 함수
    - TF-IDF와 K-Means를 사용해 클러스터링 후 계층 구조 생성
    """
    # 1. TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([' '.join(nouns)])
    
    # 2. K-Means 클러스터링
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X.T)  # 명사별 클러스터 할당
    
    # 3. 클러스터별 키워드 추출
    terms = vectorizer.get_feature_names_out()
    cluster_keywords = defaultdict(list)
    for idx, label in enumerate(labels):
        cluster_keywords[f"Cluster {label+1}"].append(terms[idx])
    
    # 4. 트리 데이터 구조 생성
    tree_data = {"name": "Root", "children": []}
    for cluster, keywords in cluster_keywords.items():
        tree_data["children"].append({
            "name": cluster,
            "children": [{"name": keyword} for keyword in keywords]
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
        title="트리 계층 구조 시각화",
        margin=dict(t=50, l=25, r=25, b=25)
    )

    # fig.show()
    img_bytes = fig.to_image(format='png')
    return img_bytes

def main(file_path):
    nouns = extract_nouns_from_text(file_path)
    cooccurrence = create_cooccurrence_matrix(nouns)
    tree_structure = build_tree_structure(nouns, n_clusters=5)

    return {
        'wordcloud': generate_wordcloud(nouns),
        'sankey': generate_sankey_diagram(cooccurrence),
        'barplot': generate_barplot(nouns),
        'tree': visualize_tree_diagram(tree_structure)
    }