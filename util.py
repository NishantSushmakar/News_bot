# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:00:32 2021

@author: nishant
"""
import os
import dialogflow_v2 as dialogflow
from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='news-bot-mytc-d8b9f12eef67.json'
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "news-bot-mytc"

def detect_intent_from_text(text,session_id,language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def get_reply(query,chat_id):
    
    response = detect_intent_from_text(query, chat_id)
    
    
    if response.intent.display_name == 'get_news':
        return 'get_news',dict(response.parameters)
    else:
        return 'small_talk',response.fulfillment_text
    
    
def fetch_news(parameters):
    
    client.language = 'english'
    client.location = parameters['geo-country']
    
    client.topic = str(parameters.get('news')[0])
    
    
    
    if (parameters.get('geo-country') != ''):
        client.location = parameters.get('geo-country')
    else :
        client.location = 'india'
    
    print(f"client language:{client.language},client location:{client.location},Client Topic:{client.topic}")
    return client.get_news()[:4]

topic_keyboard = [['Top Stories', 'World', 'Nation'], 
                   ['Business', 'Technology', 'Entertainment'], 
                   ['Sports', 'Science', 'Health']
                  ]