from flask import Flask, render_template_string
from flagsmith import Flagsmith
import json
import os

app = Flask(__name__)

# load environment key from .env file
from dotenv import load_dotenv
load_dotenv()

flagsmith = Flagsmith(environment_key=os.getenv('FLAGSMITH_ENVIRONMENT_KEY'))
# you need to set a feature on Flagsmith, conatin a json data like this: {"text": "你是天選之人，幫我測試新功能", "url": "https://example.com"} 

@app.route('/')
def home():
    flags = flagsmith.get_environment_flags()
    show_button = flags.is_feature_enabled("secret_button")
    button_data = None
    if show_button:
        feature_value = flags.get_feature_value("secret_button")
        try:
            button_data = json.loads(feature_value)
        except json.JSONDecodeError:
            print("解析按鈕的json數據時出錯。")

    html_template = '''
    <html>
    <head>
        <style>
            .btn {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                outline: none;
                color: #fff;
                background-color: #4CAF50;
                border: none;
                border-radius: 15px;
                box-shadow: 0 9px #999;
            }

            .btn:hover {background-color: #3e8e41}

            .btn:active {
                background-color: #3e8e41;
                box-shadow: 0 5px #666;
                transform: translateY(4px);
            }
        </style>
    </head>
    <body>
        <h1>假設這是Production環境</h1>
        <h2>不需重啟即可開關feature</h2>
        {% if button_data %}
            <a href="{{ button_data.url }}" class="btn">{{ button_data.text }}</a>
        {% else %}
            <p>你是一般使用者，檢視穩定的版本</p>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html_template, button_data=button_data)

if __name__ == '__main__':
    app.run(debug=True)
