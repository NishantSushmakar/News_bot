# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:12:32 2021

@author: nishant
"""
import logging
from flask import Flask,request
from telegram.ext import CommandHandler,MessageHandler,Filters,Dispatcher
from telegram import Bot,Update,ReplyKeyboardMarkup
from util import get_reply,fetch_news,topic_keyboard


logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level=logging.INFO)
logger= logging.getLogger(__name__)

TOKEN = '1569620183:AAH8m4pRnxxtoi3VbZurEJxIbYPO2qYRf10'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!'

@app.route(f'/{TOKEN}',methods= ['GET','POST'])
def webhook():
    
    update = Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "OK"

def start(update, context):
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    context.bot.send_message(update.effective_chat.id,reply)
    
def _help(update,context):
    help_txt = "Hey This is a help text!"
    context.bot.send_message(chat_id = update.effective_chat.id,text=help_txt)

def news(update,context):
    context.bot.send_message(chat_id = update.effective_chat.id,text="Choose a category",
                           reply_markup =ReplyKeyboardMarkup(keyboard=topic_keyboard, one_time_keyboard=True)   )

    
def reply_text(update,context):
    
    intent,reply= get_reply(update.message.text, update.effective_chat.id)
    
    if intent == 'get_news':
        articles =fetch_news(reply)
        
        if len(articles)>0:
            for article in articles:
                context.bot.send_message(chat_id = update.effective_chat.id,text=article['link'])
        else:
           reply_text = 'Sorry No News Found Right Now :('
           context.bot.send_message(chat_id = update.effective_chat.id,text=reply_text) 
    else:
        context.bot.send_message(chat_id = update.effective_chat.id,text=reply)
    
def echo_sticker(update,context):
    
    context.bot.send_sticker(update.effective_chat.id, update.message.sticker.file_id)

def error(bot,update):
    
    logger.error("Update '%s' caused '%s'",update,update.error)

bot =Bot(TOKEN)

try:
    bot.set_webhook("https://intense-mesa-11528.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)    
   
dp=Dispatcher(bot,None)
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CommandHandler('help',_help))
dp.add_handler(CommandHandler('news',news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
    app.run(port=8443)

    