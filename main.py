import os, httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EMAIL = "gs6817771@gmail.com"
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
        # ניסיון שליחה לשרת ה-API הראשי
        url = "https://api-global.roborock.com/api/v1/sendEmailCode"
        print(f"--- שולח בקשה למייל: {EMAIL} ---")
        
        with httpx.Client(headers=HEADERS, timeout=15.0) as client:
            resp = client.post(url, json={
                "email": EMAIL, 
                "type": "login", 
                "rr_region": "global"
            })
            
            # זה הלוג הקריטי שיעזור לנו להבין מה רובורוק אומרים
            print(f"תשובת רובורוק: סטטוס {resp.status_code}, תוכן: {resp.text}")
            
            if resp.status_code == 200:
                return jsonify({"status": "code_sent"})
            else:
                return jsonify({"status": "error", "message": resp.text})
                
    except Exception as e:
        print(f"שגיאת תקשורת: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
