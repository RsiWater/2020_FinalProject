import os
import random
import dialogflow_f

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

while True:
    texts=input('enter a text:') # targer String
    number=random.randint(0,1000) # client id(UNIQUE)
    response=dialogflow_f.detect_texts('life-nxuajt',str(number),texts,'zh-TW')
    # print(response)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(response.query_result.intent.display_name,response.query_result.intent_detection_confidence))
    print('Fulfillment text:',response.query_result.fulfillment_text)

    # if response.query_result.fulfillment_text=='哪一項服務':
    #     break
