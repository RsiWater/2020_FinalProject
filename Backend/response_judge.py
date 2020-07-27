import jieba
import datetime

def judge(response):
    origin=[['新增','加','增加','加入','記','入'],['刪除','刪'],['修改','改'],['查詢','查','查看','看']]

    intent,operate,find=0,0,False
    if response.query_result.intent.display_name=='request for account':
        intent=1
    elif response.query_result.intent.display_name=='request for schedule':
        intent=2
    elif response.query_result.intent.display_name=='request for service':
        intent=3
    else:
        intent=0

    addScore,deleteScore,updateScore,searchScore=0,0,0,0
    if response.query_result.fulfillment_text!='哪一項服務':
        for i in range(len(origin)):
            for j in origin[i]:
                if response.query_result.fulfillment_text==j:
                    operate=i+1
                    find=True
                    break
            if find==True:
                break
    else:
        jieba.add_word('後天',freq=None,tag=None)
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
            
    return intent,operate

def cutSentenceAccount(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    statusName=['收入','支出']
    date=['年','月','日','號']
    moneyName=['元','塊']
    dateNameFlag,dateFlag,moneyFlag,statusFlag,errorFlag,mouseFlag=False,False,False,False,False,False
    date_name,year,month,day,item,detail,money,status,key,user='',0,0,0,'','',0,1,0,''
    time=datetime.datetime.now()
    data=[]

    jieba.add_word('後天',freq=None,tag=None)
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
    food=['吃','喝','吃飯','飲料','飯','早餐','午餐','晚餐','餐','消夜','點心','水','酒','食','餐廳','上','菜','肉','蛋','豆','魚']
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
    timeName=['點','時','分','天','小','上午','下午','中午','晚上','凌晨','早上','到','分到','今天下午','天下']
    data=[]
    dateNameFlag,dateFlag,timeNameFlag,errorFlag,mouseFlag=False,False,False,False,False
    year,month,day,todo,key,user=0,0,0,'',0,''
    date_name,h,m,yearList,monthList,dayList=[],[],[],[],[],[]
    day_difference,m_difference,h_difference=0,0,0
    time=datetime.datetime.now()
    
    jieba.add_word('後天',freq=None,tag=None)
    words=jieba.cut(sentence,cut_all=True)
    for word in words:
        data.append(word)

    for word in data:
        try:
            print(int(word))
            try:
                if data[data.index(word)+1]=='年':
                    yearList.append(int(word))
                elif data[data.index(word)+1]=='月':
                    monthList.append(int(word))
                elif data[data.index(word)+1]=='日' or data[data.index(word)+1]=='號':
                    dayList.append(int(word))
                elif data[data.index(word)+1]=='時' or data[data.index(word)+1]=='點':
                    try:
                        if data[data.index(word)-1]=='上午' or data[data.index(word)-1]=='早上' or data[data.index(word)-1]=='凌晨':
                            h.append(int(word))
                        elif data[data.index(word)-1]=='中午':
                            h.append(12)
                        elif data[data.index(word)-1]=='下午' or data[data.index(word)-1]=='晚上':
                            h.append(int(word)+12)
                    except:
                        h.append(int(word))
                elif data[data.index(word)+1]=='分':
                    try:
                        if data[data.index(word)-1]=='點':
                            m.append(int(word))
                        else:
                            m_difference=int(word)
                    except:
                        m_difference=int(word)
                elif data[data.index(word)+1]=='天':
                    day_difference=int(word)
                elif data[data.index(word)+1]=='小':
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
            # 一段式
            todo+=word

    # year 
    if len(yearList)!=0:
        year=yearList[0]
    else:
        year=time.year
    
    # month
    if len(monthList)!=0:
        month=monthList[0]
    else:
        month=time.month
    
    # day
    if len(dayList)!=0:
        day=dayList[0]
    else:
        if len(date_name)!=0:
            if date_name[0]=='今天':
                day=time.day
            elif date_name[0]=='明天':
                day=time.day+1
            elif date_name[0]=='後天':
                day=time.day+2
            elif date_name[0]=='昨天':
                day=time.day-1
            elif date_name[0]=='前天':
                day=time.day-2
        else:
            day=time.day
    
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
                if h.index(data.index(m[0])-2)!=0:
                    m.append(0)
                    m[1]=m[0]
                    m[0]=0
                else:
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
                if date_name[len(date_name)-1]=='今天':
                    dayList.append(dayList[0])
                elif date_name[len(date_name)-1]=='明天':
                    dayList.append(dayList[0]+1)
                elif date_name[len(date_name)-1]=='後天':
                    dayList.append(dayList[0]+2)
                elif date_name[len(date_name)-1]=='昨天':
                    dayList.append(dayList[0]-1)
                elif date_name[len(date_name)-1]=='前天':
                    dayList.append(dayList[0]-2)
            elif len(date_name)==1:
                if date_name[0]=='今天':
                    dayList.append(dayList[0])
                elif date_name[0]=='明天':
                    dayList.append(dayList[0]+1)
                elif date_name[0]=='後天':
                    dayList.append(dayList[0]+2)
                elif date_name[0]=='昨天':
                    dayList.append(dayList[0]-1)
                elif date_name[0]=='前天':
                    dayList.append(dayList[0]-2)
            else:
                dayList.append(dayList[0]+day_difference)
            # h&m
            if len(h)<2:
                if len(h)==0:
                    if h_difference==0:
                        h.append(0)
                        h.append(23)
                        m.append(0)
                        m.append(59)
                    else:
                        h.append(time.hour)
                        h.append(time.hour+h_difference)
                        m.append(0)
                        m.append(0)
                else:
                    if h_difference==0:
                        if m_difference==0:
                            h.append(23)
                            m.append(0)
                            m.append(59)
                        else:
                            h.append(h[0])
                            m.append(m[0]+m_difference)
                    else:
                        if m_difference==0:
                            h.append(h[0]+h_difference)
                            m.append(0)
                            m.append(0)
                        else:
                            h.append(h[0]+h_difference)
                            m.append(m[0]+m_difference)
            if len(m)<2:
                if len(m)==0:
                    if m_difference==0:
                        m.append(0)
                        m.append(0)
                    else:
                        m.append(time.minute)
                        m.append(time.minute+m_difference)
                else:
                    if m_difference==0:
                        m.append(0)
                    else:
                        m.append(m[0]+m_difference)
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
                        h.append(0)
                        h.append(23)
                        m.append(0)
                        m.append(59)
                    else:
                        h.append(time.hour)
                        h.append(time.hour+h_difference)
                        m.append(0)
                        m.append(0)
                else:
                    if h_difference==0:
                        if m_difference==0:
                            h.append(23)
                            m.append(0)
                            m.append(59)
                        else:
                            h.append(h[0])
                            m.append(m[0]+m_difference)
                    else:
                        if m_difference==0:
                            h.append(h[0]+h_difference)
                            m.append(0)
                            m.append(0)
                        else:
                            h.append(h[0]+h_difference)
                            m.append(m[0]+m_difference)
            if len(m)<2:
                if len(m)==0:
                    if m_difference==0:
                        m.append(0)
                        m.append(0)
                    else:
                        m.append(time.minute)
                        m.append(time.minute+m_difference)
                else:
                    if m_difference==0:
                        m.append(0)
                    else:
                        m.append(m[0]+m_difference)

    return year,month,day,todo,key,user,yearList,monthList,dayList,h,m
            
            

                

            

            




            




        
        
        
        
    


    










        





    


