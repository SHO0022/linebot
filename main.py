from flask import Flask, request
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "pB3zIvFAwtNJSEWT/26TmHxMmhqO9ozTKtFpOWSKjPvGVWpIeAy738kg8gflivjQxEGY00lKuGSdoG2TilxFgG/lCMv8yZXf65sHalLTZ0x8T6qNfoiNXXfDM1QLpLFBvR2c8z0MZDOV/G/llEkXEwdB04t89/1O/w1cDnyilFU="
CLOUD_FUNCTIONS_URL = "https://predict-594289522854.asia-northeast1.run.app"


# Cloud Functions に銘柄を渡して予測を取得
def get_prediction(ticker):
    url = f"{CLOUD_FUNCTIONS_URL}?ticker={ticker}"
    res = requests.get(url)
    return res.json()


# LINE返信
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


# 整形ロジック
def format_prediction(pred):
    ticker = pred[0].get("Ticker", "不明")
    lines = [f"📈 {ticker} 最新予測\n"]

    for row in pred:
        h = row["Horizon"]
        p = row["Probability"]
        er = row["ExpectedReturn"]
        sig = row["Signal"]
        ev = row["Evidence"]

        lines.append(
            f"■ {h}日後\n"
            f"上昇確率：{p*100:.1f}%\n"
            f"期待リターン：{er*100:+.2f}%\n"
            f"シグナル：{sig}\n"
            f"エビデンス：{ev}\n"
        )

    return "\n".join(lines)


# Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    print(body)

    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message":
                reply_token = event["replyToken"]
                user_text = event["message"]["text"]  # ← ユーザーが送った銘柄

                pred = get_prediction(user_text)
                text = format_prediction(pred)

                reply_message(reply_token, text)

    return "OK"


if __name__ == "__main__":
    app.run()
