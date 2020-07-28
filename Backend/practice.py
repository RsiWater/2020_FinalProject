import jieba
import datetime
import response_judge

# sentence='吃飯'
data=[]

# words=jieba.cut(sentence,cut_all=False)
# for word in words:
#     data.append(word)

# print(data)

# time=datetime.datetime.now()

# print(type(time.year))
# print(type(time.month))
# print(type(time.day))
sentence='今天8點整吃早餐到9點半@a123#456'
jieba.add_word('後天',freq=None,tag=None)
words=jieba.cut(sentence,cut_all=True)
for word in words:
    data.append(word)

print(data)
print(response_judge.cutSentenceSchedule_add(sentence))
    
    



