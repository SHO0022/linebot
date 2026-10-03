from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "pB3zIvFAwtNJSEWT/26TmHxMmhqO9ozTKtFpOWSKjPvGVWpIeAy738kg8gflivjQxEGY00lKuGSdoG2TilxFgG/lCMv8yZXf65sHalLTZ0x8T6qNfoiNXXfDM1QLpLFBvR2c8z0MZDOV/G/llEkXEwdB04t89/1O/w1cDnyilFU="

def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, data=json.dumps(body))

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    print(body)

    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message":
                reply_token = event["replyToken"]
                user_text = event["message"]["text"]

                if "高速" in user_text:
                    reply_message(reply_token, "高速モードで処理します")
                else:
                    reply_message(reply_token, "高精度モードで処理します")

    return "OK"

if __name__ == "__main__":
    app.run()
