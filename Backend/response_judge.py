import jieba

def judge(response):
    origin=[['新增','加','增加','加入','記'],['刪除','刪'],['修改','改'],['查詢','查','查看','看']]

    intent,operate,find=0,0,False
    if response.query_result.intent.display_name=='request for account':
        intent=1
    elif response.query_result.intent.display_name=='request for schedule':
        intent=2
    elif response.query_result.intent.display_name=='request for service':
        intent=3
    else:
        intent=0

    for i in range(len(origin)):
        for j in origin[i]:
            if response.query_result.fulfillment_text==j:
                find=True
                break
        if find==True:
            operate=i+1
            break
    
    if find==False:
        # 哪一項服務
    
    return intent,operate

def cutSentenceAccount(sentence):
    dateName=['前天','昨天','今天','明天','後天']
    statusName=['收入','支出']
    date=['年','月','日','號']
    money=['元','塊']
    dateNameFlag,dateFlag,moneyFlag,statusFlag=False,False,False,False
    status_name,date_name,year,month,day,item,detail,money,status='','',0,0,0,'','',0,1
    data=[]

    words=jieba.cut(sentence,cut_all=False)
    for word in words:
        data.append(word)
    
    for i in data:
        try:
            print(int(i))
            if data[data.index(i)+1]=='年':
                year=i
            elif data[data.index(i)+1]=='月':
                month=i
            elif data[data.index(i)+1]=='日' or data[data.index(i)+1]=='號':
                day=i
            elif data[data.index(i)+1]=='元' or data[data.index(i)+1]=='塊':
                money=i
            else:
                money=i
        except:
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
            for j in money:
                if i==j:
                    moneyFlag=True
                    break
            if moneyFlag==True:
                moneyFlag=False
                continue
            for j in statusName:
                if i==j:
                    statusFlag=True
                    status_name=i
                    break
            if statusFlag==True:
                statusFlag=False
                continue
            detail=i





        





    


