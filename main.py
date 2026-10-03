from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "pB3zIvFAwtNJSEWT/26TmHxMmhqO9ozTKtFpOWSKjPvGVWpIeAy738kg8gflivjQxEGY00lKuGSdoG2TilxFgG/lCMv8yZXf65sHalLTZ0x8T6qNfoiNXXfDM1QLpLFBvR2c8z0MZDOV/G/llEkXEwdB04t89/1O/w1cDnyilFU="

CLOUD_FUNCTIONS_URL = "https://predict-594289522854.asia-northeast1.run.app"

def get_prediction():
    res = requests.get(CLOUD_FUNCTIONS_URL)
    return res.json()

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

                prediction = get_prediction()
                reply_message(reply_token, f"予測結果: {prediction}")

    return "OK"

if __name__ == "__main__":
    app.run()
