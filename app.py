from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def cohere_ai_r_plus(query, temperature=0.7, web_search=False):
    url = "https://production.api.os.cohere.ai/coral/v1/chat"
    auth = "Bearer 3DZxbNWAiBR5zYYxHNkeWUQ5jRQq5iJg53NUYr23"
    model = "command-r-plus"

    headers = {
        "Authorization": auth,
    }

    payload = {
        "message": query,
        "model": model,
        "temperature": temperature,
        "citationQuality": "CITATION_QUALITY_ACCURATE",
    }

    if web_search:
        payload["connectorsSearchOptions"] = {
            "preamble": "## Task And Context\n\nYou help people answer their questions and other requests interactively. You will be asked a very wide array of requests on all kinds of topics. You will be equipped with a wide range of search engines or similar tools to help you, which you use to research your answer. You should focus on serving the user's needs as best you can, which will be wide-ranging. The current date and time is Thursday, April 4, 2024\n\n## Style Guide\n\nUnless the user asks for a different style of answer, you should answer in full sentences, using proper grammar and spelling."
        }
        payload["connectors"] = [{"id": "web-search"}]

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return "Sorry, I couldn't understand that."
    else:    
        final_output = json.loads(response.text.strip().split('\n')[-1])["result"]["chatStreamEndEvent"]["response"]["text"]
        return final_output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    response = cohere_ai_r_plus(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)
