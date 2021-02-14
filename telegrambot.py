import requests
import json
import urllib

class TelegramBot(object):
    def __init__(self, token):
        self.BOT_URL = f"https://api.telegram.org/bot{token}/"
        self.last_id = None
    
    def delete_webhook(self):
        try:
            return requests.get(f"{self.BOT_URL}deleteWebhook")
        except requests.exceptions.ConnectionError:
            return self.no_network()
    
    def set_webhook(self, webhook):
        try:
            return requests.post(f"{self.BOT_URL}setWebhook", json={"url":webhook}).json()
        except requests.exceptions.ConnectionError:
            return self.no_network()
    
    def get_webhook(self):
        try:
            return requests.post(f"{self.BOT_URL}getWebhookInfo").json()
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_me(self):
        try:
            return requests.get(f"{self.BOT_URL}getMe").json()
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_last_update_id(self, updates):
        last_update = len(updates["result"]) - 1
        if last_update >= 0:
            self.last_id = int(updates["result"][last_update]["update_id"]) + 1

    def get_update(self):
        url = f"{self.BOT_URL}getUpdates?timeout=100"
        if self.last_id:
            url += f"&offset={self.last_id}"
        try:
            res = requests.get(url, timeout=10).json()
            return self.get_messages(res)
        except requests.exceptions.ReadTimeout:
            print("[*] Timeout")
            return 
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def get_messages(self, res):
        messages = []
        #print(res)
        for data in res["result"]:
            msg = self.get_message(data)
            messages.append(msg)
        self.get_last_update_id(res)
        return messages

    def get_message(self, data):
        message = Msg(data["message"]["text"], data["message"]["chat"]["id"], data["message"]["chat"]["first_name"])
        return message

    def send_message(self, message, chat_id):
        message = urllib.parse.quote_plus(message)
        url = self.BOT_URL + f"sendMessage?text={message}&chat_id={chat_id}"
        try:
            return requests.get(url).json()
        except requests.exceptions.ConnectionError:
            return self.no_network()

    def no_network(self):
        print("[*] No Network")
        return

class Msg(object):
    def __init__(self, message, chat_id, user):
        self.message = message
        self.chat_id = chat_id
        self.user = user
        
