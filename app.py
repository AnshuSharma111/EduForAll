from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

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
        wiki_topic = "_".join(data.split())
        wiki_link = f"https://en.wikipedia.org/wiki/{wiki_topic}"
        wiki_response = requests.get(wiki_link)
        if wiki_response.status_code == 200:
            wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
            wiki_paragraphs = wiki_soup.select('.mw-parser-output p')
            wiki_text_content = [p.get_text() for p in wiki_paragraphs][:8]
            wiki_text_content = " ".join(wiki_text_content)
            wiki_out = ""
            for word in wiki_text_content.split():
                if not word.startswith("[") and not word.endswith("]"):
                    wiki_out += word + " "
        else:
            wiki_out = 'Failed to retrieve Wikipedia content'

        # Google search processing
        google_url = f"https://www.google.com/search?q={data}"
        google_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        google_response = requests.get(google_url, headers=google_headers)
        if google_response.status_code == 200:
            google_soup = BeautifulSoup(google_response.text, 'html.parser')
            google_search_results = google_soup.find_all('div', class_='tF2Cxc')
            google_out = []
            out = ""
            for result in google_search_results:
                title = result.find('h3').text
                link = result.a['href']
                google_out.append((title, link))
            for title, link in google_out:
                out += "Title: " + title + "\nLink: " + link + "\n\n"
        else:
            out = "Failed to retrieve search results from Google"
        
        return render_template('page2.html', wiki_message=wiki_out, google_message= out)
    else:
        error_message = 'Data not found in session'
        return render_template('page2.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
    