import secret
import everytime
import time

import matplotlib.pyplot as plt

from krwordrank.word import KRWordRank
from krwordrank.word import summarize_with_keywords
from wordcloud import WordCloud


def delete_word(word):
    if "(대댓글)" in word:
        return word[5:]
    else:
        return word


def pop_keyword(keywords, popstrings):
    popwords = popstrings.split(" ")
    for i in popwords:
        try:
            keywords.pop(i)
        except:
            pass
    return keywords


font_path = 'paybooc Bold.ttf'  # font 경로

my_id = secret.secret["ID"]  # 개인의 ID 입력
my_password = secret.secret["PASSWORD"]  # 개인의 Password 입력

session = everytime.Everytime()
session.login(my_id, my_password)

texts = []

for i in range(0, 200, 20):
    print(i)
    articles = session.get_article_list(secret.freeboard_num, i)  # 크롤링 해올 게시판의 번호
    for article_dict in articles:
        texts.append(article_dict['article']['title'])
        texts.append(article_dict['article']['text'])
        for comment in article_dict['comments']:
            comment_text = comment['text']
            if comment_text == "삭제된 댓글입니다.":
                continue
            else:
                texts.append(delete_word(comment_text))
    time.sleep(1)

print(texts)

wordrank_extractor = KRWordRank(
    min_count=3,  # 단어의 최소 출현 빈도수 (그래프 생성 시)
    max_length=10,  # 단어의 최대 길이
    verbose=True
)

beta = 0.85  # PageRank의 decaying factor beta
max_iter = 10

# keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
keywords = summarize_with_keywords(texts)
for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
    print('%8s:\t%.4f' % (word, r))

krwordrank_cloud = WordCloud(
    font_path=font_path,
    width=800,
    height=800,
    background_color="white"
)
popstrings = "내가 그냥 근데 너무"
# keywords = pop_keyword(keywords, popstrings)

krwordrank_cloud = krwordrank_cloud.generate_from_frequencies(keywords)

fig = plt.figure(figsize=(10, 10))
plt.imshow(krwordrank_cloud, interpolation="bilinear")
plt.axis("off")
fig.savefig('word_cloud')

# print(text)
