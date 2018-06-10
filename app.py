import os
import sys
import json
from chatterbot import ChatBot


from datetime import datetime


import requests

from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods = ['GET'])
def verify():

	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
			return "Verification token mismatch", 403

		return request.args["hub.challenge"], 200


	return "Hello world", 200



@app.route('/', methods=['POST'])
def webhook():


	#endpint for processing


	data = request.get_json()
	#log(data)

	inteligent = False

	if data["object"] == "page":

		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:

				if messaging_event.get("message"):

					sender_id = messaging_event["sender"]["id"]
					recipient_id = messaging_event["recipient"]["id"]
					message_text = messaging_event["message"]["text"]

					if inteligent:
						chatbot = Chatbot(
							'Chalo',
							trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
							)
						chatbot.train("chatterbot.corpus.spanish")
						response = chatbot.get_response(message_text)	
						send_message(sender_id, response.text)
					else:
						send_message(sender_id, "Hola")


				if messaging_event.get("delivery"):
					pass

				if messaging_event.get("optin"):
					pass

				if messaging_event.get("postback"):
					pass

	return "ok", 200

def send_message(recipient_id, message_text):

	#log("sending message to {recipient} : {text}".format(recipient =recipient_id, text=message_text))

	params = {
		"acces_token":os.environ["PAGE_ACCES_TOKEN"]
	}
	headers = {
		"Content-Type" : "application/json"
	}

	data = json.dumps({
		"recipient": {
		"id" : recipient_id
		},
		"message":{
			"text" : message_text
		}
	})
	r = requests.post("https://graph.facebook.com/v3.0/Navollelp/messages", params=params, headers=headers, data=data)
	
	
	if r.status_code !=200:
		log(r.status_code)
		log(r.text)


def log(message):

	print (str(message))
	sys.stdout.flush()
	

if __name__ == '__main__':
	app.run(debug=True)