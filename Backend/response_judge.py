import jieba
import datetime
import json
import os
import vector

def judge(response,sentence):
    origin=[['新增','加','增加','加入','記','入'],['刪除','刪'],['修改','改'],['查詢','查','查看','看']]
    timeName=['前天','昨天','今天','明天','後天','年','月','日','號','點','時','分','小時','天','到','分到','整到','分鐘','半','整','後']
    query=[]

    intent,operate=0,0
    if response.query_result.intent.display_name=='request for account':
        intent=1
    elif response.query_result.intent.display_name=='request for schedule':
        intent=2
    elif response.query_result.intent.display_name=='request for service':
        if sentence.find('看')!=-1:
            try:
                print(sentence[sentence.find('看')+1])
                if sentence.find('元')!=-1 or sentence.find('塊')!=-1:
                    intent=1
                else:
                    intent=2
            except:
                intent=3
        else:
            if sentence.find('加總')!=-1:
                intent=1
            else:
                intent=3
    elif response.query_result.intent.display_name=='request for weather':
        intent=4
    elif response.query_result.intent.display_name=='request for receipt':
        if sentence.find('元')!=-1 or sentence.find('塊')!=-1:
            intent=1
        else:
            intent=5
    else:
        intent=0

    if intent==1 or intent==2 or intent==3:
        addScore,deleteScore,updateScore,searchScore,find=0,0,0,0,False
        if response.query_result.fulfillment_text!='哪一項服務':
            for i in range(len(origin)):
                for j in origin[i]:
                    if response.query_result.fulfillment_text==j:
                        operate=i+1
                        find=True
                        break
                if find==True:
                    break
            if find!=True:
                if sentence.find('加總')!=-1:
                    operate=4
                else:
                    operate=1
        else:
            jieba.add_word('記帳',freq=None,tag=None)
            jieba.add_word('加總',freq=None,tag=None)
            words=jieba.cut(response.query_result.query_text,cut_all=True)
            for word in words:
                query.append(word)
            scoreTable=vector.vector_model(origin,query)
            operate=scoreTable.index(max(scoreTable))+1
            # for word in words:
            #     for data in origin[0]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 addScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 addScore+=1
            #     for data in origin[1]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 deleteScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 deleteScore+=1
            #     for data in origin[2]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 updateScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 updateScore+=1
            #     for data in origin[3]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 searchScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 searchScore+=1
            
            # Score=[addScore,deleteScore,updateScore,searchScore]
            # operate=Score.index(max(Score))+1
    elif intent==4:
        operate=0
    elif intent==5:
        if sentence.find('QR')!=-1:
            operate=2
        elif sentence.find('幫')!=-1 or sentence.find('自動')!=-1:
            operate=1
        else:
            operate=0
    else:
        count,score=0,0
        accountFlag=False
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

def originJudge(response):
    origin=[['新增','加','增加','加入','記','入'],['刪除','刪'],['修改','改'],['查詢','查','查看','看']]
    query=[]
    originIntent,originOperate=0,0

    if response.query_result.intent.display_name=='request for account':
        originIntent=1
    elif response.query_result.intent.display_name=='request for schedule':
        originIntent=2
    elif response.query_result.intent.display_name=='request for service':
        originIntent=3
    elif response.query_result.intent.display_name=='request for weather':
        originIntent=4
    elif response.query_result.intent.display_name=='request for receipt':
        if response.query_result.query_text.find('元')!=-1 or response.query_result.query_text.find('塊')!=-1:
            originIntent=1
        else:
            originIntent=5
        

    if originIntent==1 or originIntent==2 or originIntent==3:
        addScore,deleteScore,updateScore,searchScore,find=0,0,0,0,False
        if response.query_result.fulfillment_text!='哪一項服務':
            for i in range(len(origin)):
                for j in origin[i]:
                    if response.query_result.fulfillment_text==j:
                        originOperate=i+1
                        find=True
                        break
                if find==True:
                    break
            if find==False:
                originOperate=1
        else:
            jieba.add_word('記帳',freq=None,tag=None)
            words=jieba.cut(response.query_result.query_text,cut_all=True)
            for word in words:
                query.append(word)
            scoreTable=vector.vector_model(origin,query)
            originOperate=scoreTable.index(max(scoreTable))+1
            # for word in words:
            #     for data in origin[0]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 addScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 addScore+=1
            #     for data in origin[1]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 deleteScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 deleteScore+=1
            #     for data in origin[2]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 updateScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 updateScore+=1
            #     for data in origin[3]:
            #         if len(word)>=len(data):
            #             if word.find(data)!=-1:
            #                 searchScore+=1
            #         else:
            #             if data.find(word)!=-1:
            #                 searchScore+=1
            
            # Score=[addScore,deleteScore,updateScore,searchScore]
            # originOperate=Score.index(max(Score))+1
    
    return originIntent,originOperate

def cutSentenceAccount(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    statusName=['收入','支出','賺','發票','中獎']
    date=['年','月','日','號']
    moneyName=['元','塊']
    otherWords=['記帳','我','想','要','想要','新增','加','增加','加入','記','入']
    tooMuchWords=['今天下午','天下','下午']
    dateNameFlag,dateFlag,moneyFlag,statusFlag,errorFlag,mouseFlag,otherWordsFlag,tooMuchFlag=False,False,False,False,False,False,False,False
    date_name,year,month,day,item,detail,money,status,key,user='',0,0,0,'','',0,1,0,''
    time=datetime.datetime.now()
    data=[]

    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('記帳',freq=None,tag=None)
    jieba.add_word('發票',freq=None,tag=None)
    jieba.add_word('中獎',freq=None,tag=None)
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
                    if i=='收入' or i=='賺' or i=='發票' or i=='中獎':
                        status=0
                    break
            if statusFlag==True:
                statusFlag=False
                continue
            for j in otherWords:
                if len(i)>=len(j):
                    if i.find(j)!=-1:
                        otherWordsFlag=True
                        break
                else:
                    if j.find(i)!=-1:
                        otherWordsFlag=True
                        break
            if otherWordsFlag==True:
                otherWordsFlag=False
                continue
            for j in tooMuchWords:
                if i==j:
                    tooMuchFlag=True
                    break
            if tooMuchFlag==True:
                tooMuchFlag=False
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
            item=classifyDetail(detail,user)
        else:
            detail='花費'
            item='其他雜項'
        return year,month,day,item,detail,money,status,key,user,errorFlag

    except:
        return year,month,day,item,detail,money,status,key,user,errorFlag

def classifyDetail(detail,user):
    check=0
    # score,maxScore=0.0,0.0
    allZeroFlag=False
    item=''
    detailBoard,scoreBoard=dict(),dict()

    scriptDir = os.path.dirname(__file__)
    folderDir = "../userTrainingData/"
    f=user+'.json'

    try:
        with open(os.path.join(scriptDir, folderDir + f),'r',encoding='utf-8') as fp:
            detailBoard=json.load(fp)
    except:
        with open(os.path.join(scriptDir, folderDir + 'detail_default.json'),'r',encoding='utf-8') as fp:
            detailBoard=json.load(fp)
    keyName=list(detailBoard.keys())

    data=[]
    for key in keyName:
        data.append(detailBoard[key])
    
    query=[]
    words=jieba.cut(detail,cut_all=False)
    for word in words:
        query.append(word)
    
    scoreTable=vector.vector_model(data,query)
    print(scoreTable)
    for score in scoreTable:
        if score==0.0:
            allZeroFlag=True
        else:
            allZeroFlag=False
            break
    if allZeroFlag==True:
        item='其他雜項'
    else:
        item=keyName[scoreTable.index(max(scoreTable))]

    # words=jieba.cut(detail,cut_all=False)
    # for word in words:
    #     for key in keyName:
    #         for data in detailBoard[key]:
    #             if len(word)>=len(data):
    #                 check=word.find(data)
    #             else:
    #                 check=data.find(word)
    #             if check!=-1:
    #                 score+=(len(word)/len(data))
    #         try:
    #             scoreBoard[key]+=score
    #         except:
    #             scoreBoard.setdefault(key,score)
    #         score=0.0
    
    # for key in keyName:
    #     if scoreBoard[key]==0.0:
    #         allZeroFlag=True
    #     else:
    #         allZeroFlag=False
    #         break
    # if allZeroFlag==False:
    #     for key in keyName:
    #         if scoreBoard[key]>maxScore:
    #             maxScore=scoreBoard[key]
    #             item=key
    # else:
    #     item='其他雜項'
        
    return item

def cutSentenceSchedule_add(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    date=['年','月','日','號']
    timeName=['點','時','分','小時','天','上午','下午','中午','晚上','凌晨','早上','到','分到','整到','今天下午','天下','分鐘','半','整','後']
    otherWords=['行程','我','想','要','想要','新增','加','增加','加入','記','入']
    data=[]
    dateNameFlag,dateFlag,timeNameFlag,mouseFlag,errorFlag,otherWordsFlag=False,False,False,False,False,False
    todo,key,user='',0,''
    date_name,h,m,yearList,monthList,dayList=[],[],[],[],[],[]
    day_difference,m_difference,h_difference,count=0,0,0,0
    time=datetime.datetime.now()
    
    # jieba切詞
    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('小時',freq=None,tag=None)
    jieba.add_word('分鐘',freq=None,tag=None)
    jieba.add_word('遊行',freq=None,tag=None)
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
            for j in otherWords:
                if len(word)>=len(j):
                    if word.find(j)!=-1:
                        otherWordsFlag=True
                        break
                else:
                    if j.find(word)!=-1:
                        otherWordsFlag=True
                        break
            if otherWordsFlag==True:
                otherWordsFlag=False
                continue
            # 一段式
            todo+=word
    
    # 是否error
    if (len(date_name)==0) and (len(yearList)==0 and len(monthList)==0 and len(dayList)==0 and len(h)==0 and len(m)==0):
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
    dateNameFlag,dateFlag,errorFlag,mouseFlag,allNameFlag,delAll,timeDel=False,False,False,False,False,False,False
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
                elif data[count]=='月' or data[count]=='月份':
                    if year==0:
                        year=time.year
                        month=int(word)
                    else:
                        month=int(word)
                elif data[count]=='日' or data[count]=='號' or data[count-2]=='月' or data[count-2]=='月份':
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

    if year!=0 or month!=0 or day!=0:
        timeDel=True

    if timeDel==False and delAll==False:
        errorFlag=True
    
    return year,month,day,key,user,timeDel,errorFlag

def cutSentence_select(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    date=['年','月','日','號']
    moneyName=['元','塊']
    allName=['全部','全','全都','所有','現有']
    operateWord=['平均','總共','總和','共','總額', '加總']
    data=[]
    dateNameFlag,dateFlag,errorFlag,mouseFlag,moneyNameFlag,moneySelect,timeSelect,allNameFlag,selectAll,operateWordFlag,avgFlag=False,False,False,False,False,False,False,False,False,False,False
    year,month,day,key,user,money,rangeJudge,operateName=0,0,0,0,'',0,'','def'
    count=0
    time=datetime.datetime.now()

    # jieba切詞
    jieba.add_word('後天',freq=None,tag=None)
    jieba.add_word('現有',freq=None,tag=None)
    jieba.add_word('總共',freq=None,tag=None)
    jieba.add_word('總和',freq=None,tag=None)
    jieba.add_word('總額',freq=None,tag=None)
    jieba.add_word("加總",freq=None,tag=None)
    words=jieba.cut(sentence,cut_all=True)
    for word in words:
        data.append(word)

    # 剔除不要的文字，留下數字、todo、key、user、money
    for word in data:
        count=count+1   #計算詞的位置
        try:
            print(int(word))
            try:
                if data[count]=='年':
                    year=int(word)
                elif data[count]=='月' or data[count]=='月份':
                    if year==0:
                        year=time.year
                        month=int(word)
                    else:
                        month=int(word)
                elif data[count]=='日' or data[count]=='號' or data[count-2]=='月' or data[count-2]=='月份':
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
                elif data[count]=='元' or data[count]=='塊':
                    money=int(word)
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
            for j in moneyName:
                if word==j:
                    moneyNameFlag=True
                    moneySelect=True
                    break
            if moneyNameFlag==True:
                moneyNameFlag=False
                continue
            for j in allName:
                if word==j:
                    allNameFlag=True
                    selectAll=True
                    break
            if allNameFlag==True:
                allNameFlag=False
                continue
            for j in operateWord:
                if word==j:
                    operateWordFlag=True
                    if word=='平均':
                        avgFlag=True
                        operateName='avg'
                    else:
                        operateName='sum'
                    break
            if operateWordFlag==True:
                operateWordFlag=False
                continue
            rangeJudge+=word

    if year!=0 or month!=0 or day!=0:
        timeSelect=True

    if avgFlag==True:
        operateName='avg'

    if timeSelect==False and moneySelect==False and selectAll==False:
        errorFlag=True
    
    if errorFlag==True and operateName!='def':
        errorFlag=False
    
    return year,month,day,key,user,money,timeSelect,moneySelect,errorFlag,rangeJudge,operateName

def cutSentence_weather(sentence):
    dateName=['今天','明天','後天']
    date=['年','月','日','號']
    week=['星期','禮拜']
    weekday=['1','2','3','4','5','6','日']
    data=[]
    dateNameFlag,dateFlag,errorFlag,mouseFlag,weekFlag,otherDayFlag=False,False,False,False,False,False
    year,month,day,key,user,dayNumber=0,0,0,0,'',0
    count=0
    time=datetime.datetime.now()

    # 先判斷是否為星期幾的語法
    for word in week:
        if sentence.find(word)!=-1:
            weekFlag=True
    
    sentence = sentence.split("@")[0]
    if weekFlag==True:
        for word in weekday:
            if sentence.find(word)!=-1:
                if word=='1':
                    dayNumber=1
                    otherDayFlag=True
                elif word=='2':
                    dayNumber=2
                    otherDayFlag=True
                elif word=="3":
                    dayNumber=3
                    otherDayFlag=True
                elif word=='4':
                    dayNumber=4
                    otherDayFlag=True
                elif word=='5':
                    dayNumber=5
                    otherDayFlag=True
                elif word=='6':
                    dayNumber=6
                    otherDayFlag=True
                elif word=='日':
                    dayNumber=7
                    otherDayFlag=True
        if otherDayFlag==False and sentence.find('天')!=-1:
            dayNumber=7
        
        num=time.isoweekday()
        if num>dayNumber:
            dayNumber=dayNumber+7
        weekDate=(time+datetime.timedelta(days=dayNumber-num)).strftime('%Y/%m/%d').split('/')
        year=int(weekDate[0])
        month=int(weekDate[1])
        day=int(weekDate[2])
    else:
        # jieba切詞
        jieba.add_word('後天',freq=None,tag=None)
        words=jieba.cut(sentence,cut_all=True)
        for word in words:
            data.append(word)

        # 剔除不要的文字，留下時間、key、user
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
                    elif data[count]=='日' or data[count]=='號' or data[count-2]=='月':
                        if year==0 and month==0:
                            year=time.year
                            month=time.month
                        elif year!=0 and month==0:
                            month=time.month
                        elif year==0 and month!=0:
                            year=time.year
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

    if year==0 and month==0 and day==0:
        year=time.year
        month=time.month
        day=time.day
    
    start_date=datetime.date(time.year,time.month,time.day)
    end_date=datetime.date(year,month,day)
    distance=end_date-start_date
    if distance.days<0 or distance.days>6:
        errorFlag=True
    
    return errorFlag,distance.days







            
            

                

            

            




            




        
        
        
        
    


    










        





    


