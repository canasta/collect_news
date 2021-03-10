import numpy as np
# from gluonnlp.data import SentencepieceTokenizer
# from kobert.utils import get_tokenizer
import kss
from konlpy.tag import Okt

from eunjeon import Mecab


def extract_nouns(news: str) -> dict:
    return extract_nouns_v2(news)


def extract_nouns_v1(news: str) -> dict:
    """Extract nouns from news.

    :param news: contents of news.
    :return: dict(). Extracted keyword and its count. {keyword: count, }
    """
    nouns = {}

    # Load tokenizer model
    # tok_path = get_tokenizer()
    # sp = SentencepieceTokenizer(tok_path)
    okt = Okt()

    news_lines = kss.split_sentences(news)

    for line in news_lines:
        # tokens = sp(line)
        tokens = okt.nouns(line)

        for token in tokens:
            if token in nouns:
                nouns[token] += 1
            else:
                nouns[token] = 1

    return nouns


def extract_nouns_v2(news: str) -> dict:
    """Extract nouns from news.

    :param news: contents of news.
    :return: dict(). Extracted keyword and its count. {keyword: count, }
    """
    nouns = {}

    mecab = Mecab()

    news_lines = kss.split_sentences(news)

    for line in news_lines:
        for st in line.split(" "):
            count = 0

            for token in mecab.nouns(st):
                nouns[token] = nouns.get(token, 0) + 1

    return nouns


def extract_keywords(group_nouns_list: list) -> list:
    """Extract keywords from the list of nouns from news groups.

    :param nouns_list: list of results of extract_nouns(). [{keyword: count, },]
    :return: list of extracted keywords. [str, ]
    """
    # Merge nouns list
    nouns_dict = dict()
    nouns_list = []
    counts_list = []
    exists_list = []
    for nouns in group_nouns_list:
        for k, v in nouns.items():
            if k in nouns_dict:
                counts_list[nouns_dict[k]] += v
                exists_list[nouns_dict[k]] += 1
            else:
                nouns_dict[k] = len(nouns_list)
                nouns_list.append(k)
                counts_list.append(v)
                exists_list.append(1)
    count = len(group_nouns_list)
    exists_list[:] = [x/count for x in exists_list]

    # Select nouns appear in more than 70% of news
    order_exist = sorted(range(len(exists_list)), key=lambda k: -exists_list[k])

    keywords = []
    count = []
    for i in order_exist:
        if exists_list[i] < 0.4 and len(keywords) > 0:
            break
        keywords.append(nouns_list[i])
        count.append(counts_list[i])

    # Sort selected keywords by counts
    order_count = sorted(range(len(count)), key=lambda k: -count[k])

    keywords[:] = [keywords[i] for i in order_count]

    return keywords


def classify_news(newslist: list) -> (list, list):
    """News comparison based on cosine similarity using KoBERT

    https://github.com/SKTBrain/KoBERT
    https://github.com/massanishi/document_similarity_algorithms_experiments

    :param newslist: list of news. [{title, desc, url}, ]
    :return: group information. each group list has sets of news index and score. [[(index, score), ], ]
    """

    # Load tokenizer model
    # tok_path = get_tokenizer()
    # sp = SentencepieceTokenizer(tok_path)
    okt = Okt()

    # Vectorize news
    _vectorized_newslist = []

    token_list = dict()
    nouns_list = []

    for news in newslist:
        # title_embeddings = [0 for _ in range(len(token_list))]
        # title_tokens = sp(news['title'])
        #
        # for token in title_tokens:
        #     if token in token_list:
        #         title_embeddings[token_list[token]] += 1
        #     else:
        #         token_list[token] = len(token_list)
        #         title_embeddings.append(1)

        desc = news['desc'].replace("<b>", "").replace("</b>", "")
        nouns = extract_nouns(desc)

        desc_embeddings = [0 for _ in range(len(token_list))]
        for noun, counts in nouns.items():
            if noun in token_list:
                desc_embeddings[token_list[noun]] = counts
            else:
                token_list[noun] = len(token_list)
                desc_embeddings.append(counts)

        # title_embeddings = np.array(title_embeddings) / np.sum(title_embeddings)
        desc_embeddings = np.array(desc_embeddings) / np.sum(desc_embeddings)

        # embeddings = desc_embeddings/2
        # for i in range(len(title_embeddings)):
        #     embeddings[i] += title_embeddings[i]/2

        # _vectorized_newslist.append(embeddings)
        _vectorized_newslist.append(desc_embeddings)

        nouns_list.append(nouns)

    # Grouping news by cosine similarity using vertor
    max_len = len(token_list)
    vectorized_newslist = [np.pad(x, (0, max_len-len(x)), mode='constant') for x in _vectorized_newslist]

    groups = []
    group_nouns = []
    checked = []

    for i in range(len(vectorized_newslist)-1):
        if i in checked:
            # Continue if already classified
            continue

        group_num = len(groups)
        groups.append([(i, 1.)])
        group_nouns.append([nouns_list[i]])
        for j in range(i+1, len(vectorized_newslist)):
            score = cosine_similarity(vectorized_newslist[i], vectorized_newslist[j])

            if score > 0.3:
                groups[group_num].append((j, score))
                group_nouns[group_num].append(nouns_list[j])
                checked.append(j)

    return groups, group_nouns


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Return cosine similarity of two vector."""
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a)*np.linalg.norm(vec_b))
