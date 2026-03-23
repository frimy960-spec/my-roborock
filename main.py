import os
import httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-global.roborock.com/api/v1"
EMAIL = "gs6817771@gmail.com"
session_storage = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    try:
        with httpx.Client() as client:
            client.post(f"{BASE_URL}/sendEmailCode", json={"email": EMAIL, "type": "login"})
            return jsonify({"status": "code_sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    try:
        with httpx.Client() as client:
            resp = client.post(f"{BASE_URL}/loginWithCode", json={
                "email": EMAIL, "code": code, "remember_me": True
            }).json()
            if "data" in resp:
                session_storage['token'] = resp['data']['token']
                return jsonify({"status": "success"})
            return jsonify({"status": "failed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/action/<cmd>')
def run_command(cmd):
    # הפקודה כרגע רק מחזירה אישור, בהמשך נחבר אותה לרובוט הספציפי
    return jsonify({"status": f"Command {cmd} received by robot"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
