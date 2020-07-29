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
sentence='3小時20分後爬山@a123#456'
# 7月29日到7月30日爬山@a123#456
# 7月29日下午4點20分到7月30日早上8點爬山@a123#456
# 2020年7月29日爬山@a123#456
# 2020年7月29日下午4點20分爬山@a123#456
# 2020年7月29日下午4點20分到晚上8點半爬山@a123#456
# 2020年7月29日下午4點20分爬山3小時40分鐘@a123#456
# 今天到明天爬山
# 今天下午4點20分到明天早上8點半爬山@a123#456
# 今天爬山@a123#456
# 今天下午4點20分爬山@a123#456
# 今天下午4點20分到晚上8點半爬山@a123#456
# 今天下午4點20分爬山3小時40分鐘@a123#456
# 3小時20分後爬山@a123#456

jieba.add_word('後天',freq=None,tag=None)
words=jieba.cut(sentence,cut_all=True)
for word in words:
    data.append(word)

print(data)
print(response_judge.cutSentenceSchedule_add(sentence))
    
    



