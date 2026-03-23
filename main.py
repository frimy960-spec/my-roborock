import os
import time
import httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-global.roborock.com/api/v1"
EMAIL = "gs6817771@gmail.com"
# משתנים לשמירת נתוני התחברות
session_data = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    try:
        with httpx.Client() as client:
            resp = client.post(f"{BASE_URL}/sendEmailCode", json={
                "email": EMAIL,
                "type": "login"
            })
            return jsonify({"status": "code_sent", "details": resp.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    try:
        with httpx.Client() as client:
            # שלב 1: התחברות עם הקוד
            login_resp = client.post(f"{BASE_URL}/loginWithCode", json={
                "email": EMAIL,
                "code": code,
                "remember_me": True
            }).json()
            
            if "data" in login_resp:
                session_data['token'] = login_resp['data']['token']
                session_data['user_id'] = login_resp['data']['userId']
                return jsonify({"status": "success"})
            return jsonify({"status": "failed", "details": login_resp})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/action/<cmd>')
def run_command(cmd):
    if 'token' not in session_data:
        return jsonify({"status": "not_logged_in"})
    
    # מיפוי פקודות פשוט
    commands = {
        "start": "app_start",
        "stop": "app_stop",
        "home": "app_charge"
    }
    
    # כאן אנחנו שולחים פקודה ישירה (מפושטת לצורך הבדיקה)
    return jsonify({"status": "feature_coming_soon", "note": "Login works, command integration in progress"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
