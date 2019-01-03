import os,sys
from flask import Flask, request
from pymessenger import Bot
import json
from imageAnalysis import img_hashtags


app = Flask(__name__)

TOKEN=#Messenger bot api token


bot=Bot(TOKEN)



@app.route('/',methods=['GET'])
def verify():
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")=="hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    global current_sentence
    global current_sentence_index
    global keyword
    global detailed_results
    global texts

    data=request.get_json()
    log(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):

                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text'].lower()

                        bot.send_text_message(sender_id,messaging_text)



                    elif 'attachments' in messaging_event['message']:
                        if messaging_event['message']['attachments'][0]['type']=='image':
                            image_url = messaging_event['message']['attachments'][0]['payload']['url']
                            hashtags=img_hashtags(image_url)
                            bot.send_text_message(sender_id,hashtags)




                    else:
                        bot.send_text_message(sender_id, "Sorry, I don't understand. :(")
                    # Echo

    return "OK", 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__=="__main__":
    app.run(debug=True, port = 80)
