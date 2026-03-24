import os, httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# גרסה 2.0 - בדיקה
@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    print("!!! הגרסה החדשה רצה - מנסה לשלוח קוד !!!")
    email = "gs6817771@gmail.com"
    url = "https://api-global.roborock.com/api/v1/sendEmailCode"
    
    headers = {
        "User-Agent": "roborock/4.3.18 (iPhone; iOS 15.1; Scale/3.00)",
        "Content-Type": "application/json"
    }
    
    try:
        with httpx.Client(headers=headers, timeout=20.0) as client:
            resp = client.post(url, json={
                "email": email, 
                "type": "login", 
                "rr_region": "global"
            })
            print(f"תשובה מרובורוק: {resp.status_code} | {resp.text}")
            return jsonify({"status": "code_sent" if resp.status_code == 200 else "error", "details": resp.text})
    except Exception as e:
        print(f"שגיאה קריטית: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
