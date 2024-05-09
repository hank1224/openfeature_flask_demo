from flask import Flask, render_template_string
from flagsmith import Flagsmith
import openfeature
from openfeature import api, client, provider
from openfeature_flagsmith.provider import FlagsmithProvider
import os

# load environment key from .env file
from dotenv import load_dotenv
load_dotenv()

# set up the FlagsmithProvider
provider = FlagsmithProvider(
    client=Flagsmith(environment_key=os.getenv('FLAGSMITH_ENVIRONMENT_KEY')),
    use_flagsmith_defaults=False,
    use_boolean_config_value=False,
    return_value_for_disabled_flags=False,
)
api.set_provider(provider)

open_feature_client = api.get_client()

# Flask app
app = Flask(__name__) 

@app.route('/')
def home():
    secret_button_feature = open_feature_client.get_boolean_value('secret_button', False) #False for prevent error
    print(secret_button_feature)

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
        {% if secret_button_feature %}
            <a href="https://example.com" class="btn">你是天選之人，幫我測試新功能</a>
        {% else %}
            <p>你是一般使用者，檢視穩定的版本</p>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html_template, secret_button_feature=secret_button_feature)

if __name__ == '__main__':
    app.run(debug=True)