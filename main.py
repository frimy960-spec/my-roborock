import os, httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EMAIL = "gs6817771@gmail.com"
# שימוש בכתובת ה-API היציבה יותר של אירופה/גלובל
BASE_URL = "https://api.roborock.com/api/v1"
HEADERS = {
    "User-Agent": "roborock/4.3.18 (iPhone; iOS 15.1; Scale/3.00)",
    "Content-Type": "application/json"
}

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    try:
        # שימוש בכתובת הספציפית לשליחת קוד
        url = "https://api-global.roborock.com/api/v1/sendEmailCode"
        with httpx.Client(headers=HEADERS, timeout=10.0) as client:
            resp = client.post(url, json={
                "email": EMAIL, 
                "type": "login", 
                "rr_region": "global"
            })
            print(f"Status: {resp.status_code}, Body: {resp.text}")
            if resp.status_code == 200:
                return jsonify({"status": "code_sent"})
            return jsonify({"status": "error", "message": resp.text})
    except Exception as e: 
        return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    # כאן נשמור את הלוגיקה להתחברות בהמשך
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
