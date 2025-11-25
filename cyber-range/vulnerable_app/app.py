from flask import Flask, request
import os
import requests
from datetime import datetime 


app = Flask(__name__)

COLLECTOR_URL = os.getenv("COLLECTOR_URL", "http://collector:8000")

def send_log(message: str, meta: dict | None = None):

    try:
        payload = {
            "source": "vulnerable_app",
            "message": message,
            "ip": request.remote_addr,
            "timestamp": datetime.utcnow().isoformat(),
            "meta": meta or {},
        }

        requests.post(f"{COLLECTOR_URL}/log", json=payload, timeout=2.0)
    except Exception as e:
        print(f"[WARN] Failed to send log: {e}")

@app.route("/")
def index():
    send_log("Homepage visited")
    return """
    <h1>Totally Safe Bank 🤡</h1>
    <p>Welcome to the most secure bank on earth (definitely not).</p>
    <p>Try visiting <a href="/login">/login</a> for a 'secure' login form.</p>
    """
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        send_log("Login page viewed")
        return """
        <h1>Login</h1>
        <form method="POST">
            <label>Username: <input name="username" /></label><br/>
            <label>Password: <input type="password" name="password" /></label><br/>
            <button type="submit">Login</button>
        </form>
        """
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # ⚠️ placeholder for future SQL injection fun
        send_log("Login attempt", meta={"username": username, "password_length": len(password)})
        return f"<p>Thanks, {username}. (We definitely didn't log your password length.)</p>"
    


    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)