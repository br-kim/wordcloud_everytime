import secret
import everytime
import time

from krwordrank.word import KRWordRank


def delete_word(word):
    if "(대댓글)" in word:
        return word[5:]
    else:
        return word


wordrank_extractor = KRWordRank(
    min_count = 3, # 단어의 최소 출현 빈도수 (그래프 생성 시)
    max_length = 10, # 단어의 최대 길이
    verbose = True
    )

beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10


my_id = secret.secret["ID"] # 개인의 ID 입력
my_password = secret.secret["PASSWORD"] # 개인의 Password 입력

session = everytime.Everytime()
session.login(my_id, my_password)

text = []

for i in range(0, 7001, 20):
    print(i)
    articles = session.get_article_list(380299, i)
    for article_dict in articles:
        text.append(article_dict['article']['title'])
        text.append(article_dict['article']['text'])
        for comment in article_dict['comments']:
            text.append(delete_word(comment['text']))
    time.sleep(1)

#print(articles)


# a = session.get_article_comment(3412956829385289)
# b = session.get_article_comment(133444176)
# print(a['article']['title'])
# print(b['article']['title'])



#print(text)
texts = text
keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)

for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    print('%8s:\t%.4f' % (word, r))

#print(text)
#sklearn
#t삭제된 댓글입니다. 제거해줘야댐.
#밑에는 1달치 결과(7000개가량)
'''
scan vocabs ...
num vocabs = 67522
done
      진짜:	145.5380
      너무:	132.7555
      그냥:	125.8984
      근데:	105.8152
      나도:	98.3306
      ㅠㅠ:	93.1483
     삭제된:	92.7873
      성적:	90.7518
      아니:	86.2044
      혹시:	80.5694
      내가:	70.6412
      저도:	67.2830
      사람:	66.6204
      ㅋㅋ:	65.3728
     교수님:	63.5874
      많이:	62.0780
     어떻게:	58.1852
      생각:	57.8825
      다들:	57.7826
      지금:	57.1579
      그럼:	51.4541
      나는:	51.2720
      저는:	50.7642
      다른:	50.5220
      하는:	48.1010
      있는:	47.5289
      그런:	46.5402
      감사:	44.3185
     그리고:	43.7490
      정말:	42.6959

Process finished with exit code 0
'''
