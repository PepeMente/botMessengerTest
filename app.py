# coding: utf-8
import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

from nltk.tokenize import sent_tokenize, word_tokenize

app = Flask(__name__)
greatings = ['bonjour','salut','coucou','ca','va']

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    
    
    

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    # Greating scenario identifiers
                    greating_detected = False 
                    g_question_detected = False
                    g_problem_detected = False
                    g_ok_detected = False
                    g_not_well_detected = False
                    g_so_so_detected = False

                    # I've got a problem scenario identifiers
                    
                    # I've got a question scenario identifiers
                    
                    # I want to order scenario identifiers
                    
                    
                    # Message response
                    response = ""
                    
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    message_text.decode("utf8")
                    sentence_tokenized = sent_tokenize(message_text)  # split the message in sentences. This is a list of string 
                    return (sentence_tokenized)                
                    number_of_sentence = len(sentence_tokenized)
                    
                    for k in range (number_of_sentence):
                        word_list = word_tokenize(sentence_tokenized[k]) # split the sentence in words. This is a list of words
                        
                        for word in word_list :
                            w = word.lower
                            sentence_length = len (word_list)
                            if w in greatings :
                                greating_detected = True
                            
                            elif word_list[sentence_length] == "?" & greating_detected == True :
                                g_question_detected = True
                               
                             
                            
                            
                            
                            if greating_detected and g_question_detected :
                                message.append("Bonjour! Je vais très bien merci, et vous :)?")
                            elif greating_detected :
                                message.append("Bonjour! comment allez vous aujourd'hui :) ?")  
                    
                    send_message(sender_id, message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
