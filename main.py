@app.route('/request_code')
def request_code():
    try:
        with httpx.Client() as client:
            # הוספנו rr_region כדי שהשרת ידע לאן לשלוח
            resp = client.post(f"{BASE_URL}/sendEmailCode", json={
                "email": EMAIL, 
                "type": "login",
                "rr_region": "global" # או "eu" אם גלובל לא עובד
            })
            print(f"Response: {resp.text}") # לוג ליתר ביטחון
            return jsonify({"status": "code_sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
