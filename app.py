from flask import Flask, render_template, request, session, redirect, url_for
import backend

app = Flask(__name__)
app.secret_key = '1qWrst7z'

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
    title = str(data).capitalize()

    if data:
        # Wikipedia processing
        wiki_out = backend.wiki_summary(data=data)

        #gpt processing
        #gpt_out = backend.chatgpt_res(data=data)

        # Google search processing
        google_out = backend.google_res(data=data)

        #Youtube links
        yt_out = backend.youtube_links(query=data)

        #google books output
        books_out = backend.google_book_search(query=data)
        
        return render_template('page2.html',title = title,google_message= google_out, youtube_message=yt_out,books_message=books_out,wiki_message=wiki_out) 
        #wiki_message=wiki_out
    else:
        error_message = 'Data not found in session'
        return render_template('page2.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)