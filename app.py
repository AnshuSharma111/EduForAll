from flask import Flask, render_template, request, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
import backend
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

API_KEY = "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"
openai.api_key = API_KEY
client = openai.OpenAI(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form.get('messageInput')
    session['data'] = data  # Store the data in the session
    return redirect(url_for('result'))

@app.route('/result')
def result():
    data = session.get('data')  # Retrieve the data from the session

    if data:
        # Wikipedia processing
        wiki_out = backend.wiki_summary(data=data)

        # Google search processing
        google_out = backend.google_res(data=data)
        
        return render_template('page2.html', wiki_message=wiki_out, google_message= google_out)
    else:
        error_message = 'Data not found in session'
        return render_template('page2.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
