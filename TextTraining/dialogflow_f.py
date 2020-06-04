import dialogflow_v2 as dialogflow

def detect_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id,session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return response