import jieba
import datetime
import response_judge

data=[]
sentence='7月份平均花了多少錢'
# scheduleAdd
# 7月29日到7月30日爬山@a123#456
# 7月29日下午4點20分到7月30日早上8點爬山@a123#456
# 2020年7月29日爬山@a123#456
# 2020年7月29日下午4點20分爬山@a123#456
# 2020年7月29日下午4點20分到晚上8點半打電腦@a123#456
# 2020年7月29日下午4點20分爬山3小時40分鐘@a123#456
# 今天到明天爬山
# 今天下午4點20分到明天早上8點半爬山@a123#456
# 今天爬山@a123#456
# 今天下午4點20分爬山@a123#456
# 今天下午4點20分到晚上8點半爬山@a123#456
# 今天下午4點20分爬山3小時40分鐘@a123#456
# 3小時20分後爬山@a123#456
# 今天2020年7月29日下午4點20分爬山3天@a123#456
# 今天到7月30日爬山@a123#456

# delete
# 7月30日@a123#456
# 7月@a123#456
# 2020年@a123#456
# 全部刪除@a123#456
# 我要刪除@a123#456
jieba.add_word('後天',freq=None,tag=None)
jieba.add_word('小時',freq=None,tag=None)
jieba.add_word('分鐘',freq=None,tag=None)
jieba.add_word('現有',freq=None,tag=None)
jieba.add_word('記帳',freq=None,tag=None)
words=jieba.cut(sentence,cut_all=True)
for word in words:
    data.append(word)

print(data)
# print(response_judge.cutSentence_select(sentence))

    
    



