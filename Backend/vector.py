import math

def vector_model(data,query):
    # TF
    tf=[]
    for seg in data:
        tf_data={}
        words=[]
        for word in seg:
            tf_data[word]=tf_data.get(word,0)+1
        for word in seg:
            if word not in words:
                tf_data[word]=tf_data[word]/len(seg)
                words.append(word)
        tf.append(tf_data)

    # IDF
    idf_data=[]
    for seg in data:
        for word in seg:
            if word not in idf_data:
                idf_data.append(word)
    
    idf={}
    for i in idf_data:
        for j in tf:
            if j.get(i,0)!=0:
                idf[i]=idf.get(i,0)+1
        num=idf[i]
        idf[i]=1+math.log(len(data)/num)
    
    # QueryWeight
    query_tf,query_weight={},{}
    q_words=[]
    for word in query:
        query_tf[word]=query_tf.get(word,0)+1
        query_weight[word]=query_weight.get(word,0)
    for word in query:
        if word not in q_words:
            query_tf[word]=query_tf[word]/len(query)
            q_words.append(word)
    for word in query:
        for seg in tf:
            for key in list(seg.keys()):
                if len(word)>=len(key):
                    check=word.find(key)
                else:
                    check=key.find(word)
                if check!=-1:
                    query_weight[word]=query_tf.get(word,0)*idf.get(key,0)
                    break
            if query_weight[word]!=0:
                break
    
    # Similarity
    scoreTable=[]
    for seg in tf:
        sum_cross=0
        sum_query=0
        sum_data=0

        # sum_cross
        for word in query:
            for key in list(seg.keys()):
                if len(word)>=len(key):
                    check=word.find(key)
                else:
                    check=key.find(word)
                if check!=-1:
                    data_weight=seg.get(key,0)*idf.get(key,0)
                    sum_cross=sum_cross+data_weight*query_weight[word]
        
        # sum_query
        for word in query:
            sum_query=sum_query+query_weight[word]**2
        
        # sum_data
        for key in list(seg.keys()):
            data_weight=seg.get(key,0)*idf.get(key,0)
            sum_data=sum_data+data_weight**2

        # CountScore
        try:
            score=sum_cross/((sum_query**0.5)*(sum_data**0.5))
        except:
            score=0
        scoreTable.append(score)
        
    return scoreTable

        





        