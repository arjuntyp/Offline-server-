from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Facebook Cookie to Token</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');

  body {
    margin: 0;
    height: 100vh;
    font-family: 'Orbitron', sans-serif;
    background: url('https://images.unsplash.com/photo-1530639836360-26a3b4cd29f7?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
    background-size: cover;
    color: #00fff7;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  .container {
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid #00fff7;
    padding: 30px;
    border-radius: 15px;
    width: 600px;
    text-align: center;
    box-shadow: 0 0 20px #00fff7;
    animation: neonGlow 1.5s ease-in-out infinite alternate;
  }

  @keyframes neonGlow {
    from {
      box-shadow: 0 0 10px #00fff7, 0 0 20px #00fff7, 0 0 30px #00fff7;
    }
    to {
      box-shadow: 0 0 20px #0ff, 0 0 40px #0ff, 0 0 60px #0ff;
    }
  }

  textarea {
    width: 100%;
    height: 120px;
    border-radius: 8px;
    border: 1.5px solid #00fff7;
    background: #001f21c9;
    color: #00fff7;
    font-family: monospace;
    font-size: 14px;
    padding: 12px;
    resize: vertical;
    outline: none;
    transition: 0.3s;
  }
  textarea:focus {
    border-color: #00f9ff;
    box-shadow: 0 0 10px #00f9ff;
  }
  button {
    margin-top: 15px;
    padding: 12px 25px;
    font-size: 18px;
    border-radius: 30px;
    border: 2px solid #00fff7;
    color: #00fff7;
    background: transparent;
    cursor: pointer;
    font-weight: bold;
    transition: 0.3s;
  }
  button:hover {
    background: #00fff7;
    color: black;
    box-shadow: 0 0 25px #00fff7;
  }
  pre {
    margin-top: 20px;
    text-align: left;
    background: #002629cc;
    border: 1.5px solid #00fff7;
    padding: 20px;
    border-radius: 12px;
    font-size: 14px;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
</style>
</head>
<body>
<div class="container">
  <h1>Facebook Cookie से Token निकालें</h1>
  <form method="POST" action="/">
    <textarea name="cookie" placeholder="यहीं अपनी Facebook cookie paste करें..." required>{{ cookie|default('') }}</textarea>
    <br />
    <button type="submit">Token Generate करें</button>
  </form>

  {% if token %}
    <pre>Token: {{ token }}</pre>
  {% elif error %}
    <pre style="color:#ff4444;">{{ error }}</pre>
  {% endif %}
</div>
</body>
</html>
'''

def get_fb_token(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; vivo 1610 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FBAN/Orca-Android;FBAV/295.0.0.42.119]",
        "Content-Type": "application/x-www-form-urlencoded",
        "cookie": cookie
    }
    url = "https://business.facebook.com/business_locations"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200 and ("EAAG" in resp.text or "EAAD" in resp.text):
            token = None
            for prefix in ["EAAG", "EAAD"]:
                if f'","accessToken":"{prefix}' in resp.text:
                    token = resp.text.split(f'","accessToken":"{prefix}')[1].split('"')[0]
                    token = f"{prefix}{token}"
                    return token
            return None
        else:
            return None
    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    token = None
    error = None
    cookie = ""
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        if cookie:
            token = get_fb_token(cookie)
            if not token:
                error = "Token नहीं मिला। कृपया सही cookie डालें या method patch हो सकता है।"
        else:
            error = "कृपया cookie डाले।"
    return render_template_string(HTML, token=token, error=error, cookie=cookie)

if __name__ == '__main__':
    app.run(port=5000)
