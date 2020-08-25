import jieba
import datetime

def judge(response,sentence):
    origin=[['新增','加','增加','加入','記','入'],['刪除','刪'],['修改','改'],['查詢','查','查看','看']]
    timeName=['前天','昨天','今天','明天','後天','年','月','日','號','點','時','分','小時','天','上午','下午','中午','晚上','凌晨','早上','到','分到','整到','今天下午','天下','分鐘','半','整','後']

    intent,operate=0,0
    if response.query_result.intent.display_name=='request for account':
        intent=1
    elif response.query_result.intent.display_name=='request for schedule':
        intent=2
    elif response.query_result.intent.display_name=='request for service':
        intent=3
    else:
        intent=0

    if intent!=0:
        addScore,deleteScore,updateScore,searchScore,find=0,0,0,0,False
        if response.query_result.fulfillment_text!='哪一項服務' and intent!=3:
            for i in range(len(origin)):
                for j in origin[i]:
                    if response.query_result.fulfillment_text==j:
                        operate=i+1
                        find=True
                        break
                if find==True:
                    break
        else:
            jieba.add_word('記帳',freq=None,tag=None)
            words=jieba.cut(response.query_result.query_text,cut_all=True)
            for word in words:
                for data in origin[0]:
                    if len(word)>=len(data):
                        if word.find(data)!=-1:
                            addScore+=1
                    else:
                        if data.find(word)!=-1:
                            addScore+=1
                for data in origin[1]:
                    if len(word)>=len(data):
                        if word.find(data)!=-1:
                            deleteScore+=1
                    else:
                        if data.find(word)!=-1:
                            deleteScore+=1
                for data in origin[2]:
                    if len(word)>=len(data):
                        if word.find(data)!=-1:
                            updateScore+=1
                    else:
                        if data.find(word)!=-1:
                            updateScore+=1
                for data in origin[3]:
                    if len(word)>=len(data):
                        if word.find(data)!=-1:
                            searchScore+=1
                    else:
                        if data.find(word)!=-1:
                            searchScore+=1
            
            Score=[addScore,deleteScore,updateScore,searchScore]
            operate=Score.index(max(Score))+1
    else:
        accountFlag,count,score=False,0,0
        cutwords=[]
        words=jieba.cut(sentence,cut_all=True)
        for word in words:
            cutwords.append(word)
        
        for word in cutwords:
            if (word=='元' or word=='塊') and count!=0:
                try:
                    print(int(cutwords[count-1]))
                    accountFlag=True
                    break
                except:
                    count+=1
            else:
                for i in timeName:
                    if word==i:
                        score+=1
                        break
            count+=1
        
        if accountFlag==True:
            intent=1
        else:
            if score>0:
                intent=2
            else:
                intent=0
        if intent!=0:
            operate=1

    return intent,operate

def cutSentenceAccount(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    statusName=['收入','支出']
    date=['年','月','日','號']
    moneyName=['元','塊']
    oneName=['新增','記帳','我','想','要','想要']
    dateNameFlag,dateFlag,moneyFlag,statusFlag,errorFlag,mouseFlag,oneNameFlag=False,False,False,False,False,False,False
    date_name,year,month,day,item,detail,money,status,key,user='',0,0,0,'','',0,1,0,''
    time=datetime.datetime.now()
    data=[]

    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('記帳',freq=None,tag=None)
    words=jieba.cut(sentence,cut_all=True)
    for word in words:
        data.append(word)
    
    print(data)
    
    for i in data:
        try:
            print(int(i))
            try:
                if data[data.index(i)+1]=='年':
                    year=int(i)
                elif data[data.index(i)+1]=='月':
                    month=int(i)
                elif data[data.index(i)+1]=='日' or data[data.index(i)+1]=='號':
                    day=int(i)
                elif data[data.index(i)+1]=='元' or data[data.index(i)+1]=='塊':
                    money=int(i)
                else:
                    money=int(i)
            except:
                key=int(i)
        except:
            if i=='@':
                mouseFlag=True
                continue
            if i=='#':
                continue
            if mouseFlag==True:
                user=i
                mouseFlag=False
                continue

            for j in dateName:
                if i==j:
                    dateNameFlag=True
                    date_name=i
                    break
            if dateNameFlag==True:
                dateNameFlag=False
                continue
            for j in date:
                if i==j:
                    dateFlag=True
                    break
            if dateFlag==True:
                dateFlag=False
                continue
            for j in moneyName:
                if i==j:
                    moneyFlag=True
                    break
            if moneyFlag==True:
                moneyFlag=False
                continue
            for j in statusName:
                if i==j:
                    statusFlag=True
                    if i=='收入':
                        status=0
                    break
            if statusFlag==True:
                statusFlag=False
                continue
            for j in oneName:
                if i==j:
                    oneNameFlag=True
                    break
            if oneNameFlag==True:
                oneNameFlag=False
                continue
            # 一段式
            detail+=i
        
    try:
        # 判斷錢
        if money==0:
            errorFlag=True
            print(int('error'))

        # 判斷時間
        if len(date_name)!=0:
            if date_name=='今天':
                year=time.year
                month=time.month
                day=time.day
            elif date_name=='明天':
                year=time.year
                month=time.month
                day=time.day+1
            elif date_name=='後天':
                year=time.year
                month=time.month
                day=time.day+2
            elif date_name=='昨天':
                year=time.year
                month=time.month
                day=time.day-1
            elif date_name=='前天':
                year=time.year
                month=time.month
                day=time.day-2
        else:
            if year==0 and month==0 and day==0:
                year=time.year
                month=time.month
                day=time.day
            else:
                if year==0:
                    year=time.year
                if month==0:
                    month=time.month
                if day==0:
                    day=time.day
        
        # 判斷細項
        if len(detail)!=0:
            item=classifyDetail(detail)
        else:
            detail='花費'
            item='其他雜項'
        return year,month,day,item,detail,money,status,key,user,errorFlag

    except:
        return year,month,day,item,detail,money,status,key,user,errorFlag


def classifyDetail(detail):
    leisure=['上','去','游泳','健身房','遊樂園','看','展覽','電影','館','點卡','點數','遊戲','玩具','模型','球','漫畫','書']
    transportation=['車','車票','火車','高鐵','坐','搭','公車','交通','運輸','捷運','加','油','大眾']
    learn=['書','講義','補習','教材','課','上']
    health=['看','病','醫','療','護','健康','保健','藥']
    assurance=['保','保險','險','股票','股','賣']
    food=['吃','喝','吃飯','飲料','飯','早餐','午餐','晚餐','餐','宵夜','點心','水','酒','食','餐廳','上','菜','肉','蛋','豆','魚']
    otherScore,leisureScore,transportationScore,learnScore,healthScore,assuranceScore,foodScore=0,0,0,0,0,0,0
    item=''

    words=jieba.cut(detail,cut_all=False)
    for word in words:
        for data in leisure:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    leisureScore+=1
            else:
                if data.find(word)!=-1:
                    leisureScore+=1
        for data in transportation:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    transportationScore+=1
            else:
                if data.find(word)!=-1:
                    transportationScore+=1
        for data in learn:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    learnScore+=1
            else:
                if data.find(word)!=-1:
                    learnScore+=1
        for data in health:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    healthScore+=1
            else:
                if data.find(word)!=-1:
                    healthScore+=1
        for data in assurance:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    assuranceScore+=1
            else:
                if data.find(word)!=-1:
                    assuranceScore+=1
        for data in food:
            if len(word)>=len(data):
                if word.find(data)!=-1:
                    foodScore+=1
            else:
                if data.find(word)!=-1:
                    foodScore+=1
        
    Score=[otherScore,leisureScore,transportationScore,learnScore,healthScore,assuranceScore,foodScore]
    if Score.index(max(Score))==0:
        item='其他雜項'
    elif Score.index(max(Score))==1:
        item='休閒娛樂'
    elif Score.index(max(Score))==2:
        item='行車交通'
    elif Score.index(max(Score))==3:
        item='進修學習'
    elif Score.index(max(Score))==4:
        item='醫療保健'
    elif Score.index(max(Score))==5:
        item='金融保險'
    elif Score.index(max(Score))==6:
        item='食品酒水'
    return item


def cutSentenceSchedule_add(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    date=['年','月','日','號']
    timeName=['點','時','分','小時','天','上午','下午','中午','晚上','凌晨','早上','到','分到','整到','今天下午','天下','分鐘','半','整','後']
    oneName=['新增','行程','我','想','要','想要','事情','提醒']
    data=[]
    dateNameFlag,dateFlag,timeNameFlag,mouseFlag,errorFlag,oneNameFlag=False,False,False,False,False,False
    todo,key,user='',0,''
    date_name,h,m,yearList,monthList,dayList=[],[],[],[],[],[]
    day_difference,m_difference,h_difference,count=0,0,0,0
    time=datetime.datetime.now()
    
    # jieba切詞
    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('小時',freq=None,tag=None)
    jieba.add_word('分鐘',freq=None,tag=None)
    words=jieba.cut(sentence,cut_all=True)
    for word in words:
        data.append(word)

    # 剔除不要的文字，留下數字、todo、key、user
    for word in data:
        count=count+1   #計算詞的位置
        try:
            print(int(word))
            try:
                if data[count]=='年':
                    yearList.append(int(word))
                elif data[count]=='月':
                    monthList.append(int(word))
                elif data[count]=='日' or data[count]=='號' or data[count-2]=='月':
                    dayList.append(int(word))
                elif data[count]=='時' or data[count]=='點':
                    try:
                        if data[count-2]=='上午' or data[count-2]=='早上' or data[count-2]=='凌晨' or data[count-2]=='中午':
                            h.append(int(word))
                        elif data[count-2]=='下午' or data[count-2]=='晚上':
                            h.append(int(word)+12)
                        else:
                            h.append(int(word))
                    except:
                        h.append(int(word))
                elif data[count]=='分' or data[count]=='分鐘':
                    try:
                        if data[count-2]=='點' or data[count-2]=='時':
                            m.append(int(word))
                        else:
                            m_difference=int(word)
                    except:
                        m_difference=int(word)
                elif data[count]=='天':
                    day_difference=int(word)
                elif data[count]=='小時':
                    h_difference=int(word)
                else:
                    m.append(int(word))
            except:
                key=int(word)
        except:
            if word=='@':
                mouseFlag=True
                continue
            if word=='#':
                continue
            if mouseFlag==True:
                user=word
                mouseFlag=False
                continue
            if word=='半':
                m.append(30)
                # data[data.index(word)]='30'
                continue

            for j in dateName:
                if word==j:
                    dateNameFlag=True
                    date_name.append(word)
                    break
            if dateNameFlag==True:
                dateNameFlag=False
                continue
            for j in date:
                if word==j:
                    dateFlag=True
                    break
            if dateFlag==True:
                dateFlag=False
                continue
            for j in timeName:
                if word==j:
                    timeNameFlag=True
                    break
            if timeNameFlag==True:
                timeNameFlag=False
                continue
            for j in oneName:
                if word==j:
                    oneNameFlag=True
                    break
            if oneNameFlag==True:
                oneNameFlag=False
                continue
            # 一段式
            todo+=word
    
    # 是否error
    if len(date_name)==0 and (len(yearList)==0 and len(monthList)==0 and len(dayList)==0 and len(h)==0 and len(m)==0):
        errorFlag=True
    # start&end
    if len(dayList)>=2:
        if len(monthList)<2:
            while True:
                monthList.append(time.month)
                if len(monthList)==2:
                    break
        if len(yearList)<2:
            while True:
                yearList.append(time.year)
                if len(yearList)==2:
                    break
        if len(h)<2:
            if len(h)==0:
                h.append(0)
                h.append(23)
                m.append(0)
                m.append(59)
            else:
                if len(m)==0:
                    h.append(23)
                    m.append(0)
                    m.append(59)
                else:
                    h.append(23)
                    m.append(59)
        if len(m)<2:
            if len(m)==0:
                m.append(0)
                m.append(0)
            else:
                try:
                    if h.index(int(data[data.index(str(m[0]))-2]))!=0:
                        m.append(0)
                        m[1]=m[0]
                        m[0]=0
                    else:
                        m.append(0)
                except:
                    m.append(0)
    else:
        if len(dayList)==1:
            # month&year
            if len(monthList)<2:
                while True:
                    monthList.append(time.month)
                    if len(monthList)==2:
                        break
            if len(yearList)<2:
                while True:
                    yearList.append(time.year)
                    if len(yearList)==2:
                        break
            # day
            if len(date_name)>=2:
                for i in range(len(date_name)):
                    if date_name[i]=='今天':
                        if dayList[0]!=time.day:
                            dayList.append(time.day)
                    elif date_name[i]=='明天':
                        if dayList[0]!=time.day+1:
                            dayList.append(time.day+1)
                    elif date_name[i]=='後天':
                        if dayList[0]!=time.day+2:
                            dayList.append(time.day+2)
                    elif date_name[i]=='昨天':
                        if dayList[0]!=time.day-1:
                            dayList.append(time.day-1)
                    elif date_name[i]=='前天':
                        if dayList[0]!=time.day-2:
                            dayList.append(time.day-2)
            elif len(date_name)==1:
                if date_name[0]=='今天':
                    if dayList[0]!=time.day:
                        dayList.append(time.day)
                    else:
                        dayList.append(dayList[0]+day_difference)
                elif date_name[0]=='明天':
                    if dayList[0]!=time.day+1:
                        dayList.append(time.day+1)
                    else:
                        dayList.append(dayList[0]+day_difference)
                elif date_name[0]=='後天':
                    if dayList[0]!=time.day+2:
                        dayList.append(time.day+2)
                    else:
                        dayList.append(dayList[0]+day_difference)
                elif date_name[0]=='昨天':
                    if dayList[0]!=time.day-1:
                        dayList.append(time.day-1)
                    else:
                        dayList.append(dayList[0]+day_difference)
                elif date_name[0]=='前天':
                    if dayList[0]!=time.day-2:
                        dayList.append(time.day-2)
                    else:
                        dayList.append(dayList[0]+day_difference)
            else:
                dayList.append(dayList[0]+day_difference)
            # h&m
            if len(h)<2:
                if len(h)==0:
                    if h_difference==0:
                        if m_difference==0:
                            h.append(0)
                            h.append(23)
                            m.append(0)
                            m.append(59)
                        else:
                            if time.minute+m_difference>=60:   
                                h.append(time.hour+(time.minute+m_difference)/60)
                                m.append((time.minute+m_difference)%60)
                                h.append(23)
                                m.append(59)
                            else:
                                h.append(time.hour)
                                m.append(time.minute+m_difference)
                                h.append(23)
                                m.append(59)
                    else:
                        if m_difference==0:
                            h.append(time.hour+h_difference)
                            m.append(time.minute)
                            h.append(23)
                            m.append(59)
                        else:
                            if time.minute+m_difference>=60:   
                                h.append(time.hour+(time.minute+m_difference)/60+h_difference)
                                m.append((time.minute+m_difference)%60)
                                h.append(23)
                                m.append(59)
                            else:
                                h.append(time.hour+h_difference)
                                m.append(time.minute+m_difference)
                                h.append(23)
                                m.append(59)
                else:
                    if h_difference==0:
                        if m_difference==0:
                            if len(m)==0:
                                h.append(23)
                                m.append(0)
                                m.append(59)
                            else:
                                h.append(23)
                                m.append(59)
                        else:
                            if len(m)==0:
                                m.append(0)
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0])
                                    m.append(m[0]+m_difference)
                            else:
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0])
                                    m.append(m[0]+m_difference)
                    else:
                        if m_difference==0:
                            if len(m)==0:
                                h.append(h[0]+h_difference)
                                m.append(0)
                                m.append(0)
                            else:
                                h.append(h[0]+h_difference)
                                m.append(m[0])
                        else:
                            if len(m)==0:
                                m.append(0)
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60+h_difference)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0]+h_difference)
                                    m.append(m[0]+m_difference)
                            else:
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60+h_difference)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0]+h_difference)
                                    m.append(m[0]+m_difference)
            if len(m)<2:
                if len(m)==0:
                    m.append(0)
                    m.append(0)
                else:
                    try:
                        if h.index(int(data[data.index(str(m[0]))-2]))!=0:
                            m.append(0)
                            m[len(m)-1]=m[0]
                            m[0]=0
                        else:
                            m.append(0)
                    except:
                        m.append(0)
        else:
            # month&year
            if len(monthList)<2:
                while True:
                    monthList.append(time.month)
                    if len(monthList)==2:
                        break
            if len(yearList)<2:
                while True:
                    yearList.append(time.year)
                    if len(yearList)==2:
                        break
            # day
            if len(date_name)>=2:
                if date_name[0]=='今天':
                    dayList.append(time.day)
                elif date_name[0]=='明天':
                    dayList.append(time.day+1)
                elif date_name[0]=='後天':
                    dayList.append(time.day+2)
                elif date_name[0]=='昨天':
                    dayList.append(time.day-1)
                elif date_name[0]=='前天':
                    dayList.append(time.day-2)
                
                if date_name[len(date_name)-1]=='今天':
                    dayList.append(time.day)
                elif date_name[len(date_name)-1]=='明天':
                    dayList.append(time.day+1)
                elif date_name[len(date_name)-1]=='後天':
                    dayList.append(time.day+2)
                elif date_name[len(date_name)-1]=='昨天':
                    dayList.append(time.day-1)
                elif date_name[len(date_name)-1]=='前天':
                    dayList.append(time.day-2)
            elif len(date_name)==1:
                if date_name[0]=='今天':
                    dayList.append(time.day)
                elif date_name[0]=='明天':
                    dayList.append(time.day+1)
                elif date_name[0]=='後天':
                    dayList.append(time.day+2)
                elif date_name[0]=='昨天':
                    dayList.append(time.day-1)
                elif date_name[0]=='前天':
                    dayList.append(time.day-2)
                
                dayList.append(dayList[0]+day_difference)
            else:
                dayList.append(time.day)
                dayList.append(dayList[0]+day_difference)
            # h&m
            if len(h)<2:
                if len(h)==0:
                    if h_difference==0:
                        if m_difference==0:
                            h.append(0)
                            h.append(23)
                            m.append(0)
                            m.append(59)
                        else:
                            if time.minute+m_difference>=60:   
                                h.append(time.hour+(time.minute+m_difference)/60)
                                m.append((time.minute+m_difference)%60)
                                h.append(23)
                                m.append(59)
                            else:
                                h.append(time.hour)
                                m.append(time.minute+m_difference)
                                h.append(23)
                                m.append(59)
                    else:
                        if m_difference==0:
                            h.append(time.hour+h_difference)
                            m.append(time.minute)
                            h.append(23)
                            m.append(59)
                        else:
                            if time.minute+m_difference>=60:   
                                h.append(time.hour+(time.minute+m_difference)/60+h_difference)
                                m.append((time.minute+m_difference)%60)
                                h.append(23)
                                m.append(59)
                            else:
                                h.append(time.hour+h_difference)
                                m.append(time.minute+m_difference)
                                h.append(23)
                                m.append(59)
                else:
                    if h_difference==0:
                        if m_difference==0:
                            if len(m)==0:
                                h.append(23)
                                m.append(0)
                                m.append(59)
                            else:
                                h.append(23)
                                m.append(59)
                        else:
                            if len(m)==0:
                                m.append(0)
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0])
                                    m.append(m[0]+m_difference)
                            else:
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0])
                                    m.append(m[0]+m_difference)
                    else:
                        if m_difference==0:
                            if len(m)==0:
                                h.append(h[0]+h_difference)
                                m.append(0)
                                m.append(0)
                            else:
                                h.append(h[0]+h_difference)
                                m.append(m[0])
                        else:
                            if len(m)==0:
                                m.append(0)
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60+h_difference)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0]+h_difference)
                                    m.append(m[0]+m_difference)
                            else:
                                if m[0]+m_difference>=60:   
                                    h.append(h[0]+(m[0]+m_difference)/60+h_difference)
                                    m.append((m[0]+m_difference)%60)
                                else:
                                    h.append(h[0]+h_difference)
                                    m.append(m[0]+m_difference)
            if len(m)<2:
                print('check')
                if len(m)==0:
                    m.append(0)
                    m.append(0)
                else:
                    print('check')
                    try:
                        if h.index(int(data[data.index(str(m[0]))-2]))!=0:
                            m.append(0)
                            m[len(m)-1]=m[0]
                            m[0]=0
                        else:
                            print('yeah')
                            m.append(0)
                    except:
                        print('no')
                        m.append(0)


    # 去float
    for i in range(len(h)):
        h[i]=int(h[i])
    for i in range(len(m)):
        m[i]=int(m[i])
    
    # start<end
    if dayList[0]>dayList[len(dayList)-1] and monthList[0]==monthList[len(dayList)-1]:
        tmp=dayList[0]
        dayList[0]=dayList[len(dayList)-1]
        dayList[len(dayList)-1]=tmp
    if monthList[0]>monthList[len(monthList)-1]:
        tmp=monthList[0]
        monthList[0]=monthList[len(monthList)-1]
        monthList[len(monthList)-1]=tmp
    if yearList[0]>yearList[len(yearList)-1]:
        tmp=yearList[0]
        yearList[0]=yearList[len(yearList)-1]
        yearList[len(yearList)-1]=tmp

    return todo,key,user,yearList,monthList,dayList,h,m,errorFlag


def cutSentence_del(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    date=['年','月','日','號']
    allName=['全部','全','全都','所有','現有']
    data=[]
    dateNameFlag,dateFlag,errorFlag,mouseFlag,allNameFlag,delAll=False,False,False,False,False,False
    year,month,day,key,user=0,0,0,0,''
    count=0
    time=datetime.datetime.now()

    # jieba切詞
    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('現有',freq=None,tag=None)
    words=jieba.cut(sentence,cut_all=True)
    for word in words:
        data.append(word)

    # 剔除不要的文字，留下數字、todo、key、user
    for word in data:
        count=count+1   #計算詞的位置
        try:
            print(int(word))
            try:
                if data[count]=='年':
                    year=int(word)
                elif data[count]=='月':
                    if year==0:
                        year=time.year
                        month=int(word)
                    else:
                        month=int(word)
                elif data[count]=='日' or data[count]=='號' or data[count-2]=='月':
                    if year==0 and month==0:
                        year=time.year
                        month=time.month
                        day=int(word)
                    elif year!=0 and month==0:
                        month=time.month
                        day=int(word)
                    elif year==0 and month!=0:
                        year=time.year
                        day=int(word)
                    else:
                        day=int(word)
                else:
                    day=int(word)
            except:
                key=int(word)
        except:
            if word=='@':
                mouseFlag=True
                continue
            if word=='#':
                continue
            if mouseFlag==True:
                user=word
                mouseFlag=False
                continue

            for j in dateName:
                if word==j:
                    if word=='今天':
                        year=time.year
                        month=time.month
                        day=time.day
                    elif word=='前天':
                        year=time.year
                        month=time.month
                        day=time.day-2
                    elif word=='昨天':
                        year=time.year
                        month=time.month
                        day=time.day-1
                    elif word=='明天':
                        year=time.year
                        month=time.month
                        day=time.day+1
                    elif word=='後天':
                        year=time.year
                        month=time.month
                        day=time.day+2
                    dateNameFlag=True
                    break
            if dateNameFlag==True:
                dateNameFlag=False
                continue
            for j in date:
                if word==j:
                    dateFlag=True
                    break
            if dateFlag==True:
                dateFlag=False
                continue
            for j in allName:
                if word==j:
                    allNameFlag=True
                    delAll=True
                    break
            if allNameFlag==True:
                allNameFlag=False
                continue

    if year==0 and month==0 and day==0 and delAll==False:
        errorFlag=True
    
    return year,month,day,key,user,delAll,errorFlag
    
            






            
            

                

            

            




            




        
        
        
        
    


    










        





    


