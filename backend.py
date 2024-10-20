import re
import requests
from bs4 import BeautifulSoup
from pytube import Search

#API for chatGPT
# API_KEY = "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"
# client = openai.OpenAI(api_key=API_KEY)


def load_inappropriate_words(file_path: str) -> list:
    """Read inappropriate words from a text file and return as a list."""
    try:
        with open(file_path, 'r') as file:
            words = [line.strip().lower() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print("Inappropriate words file not found.")
        return []

# Load inappropriate words once when the backend starts
INAPPROPRIATE_WORDS = load_inappropriate_words('inappropriate_words.txt')

def contains_inappropriate_words(query: str) -> bool:
    """Check if the query contains any inappropriate words."""
    query = query.lower()  # Convert query to lowercase
    query_words = query.split()  # Split the query into words
    for word in query_words:
        if word in INAPPROPRIATE_WORDS:
            return True  # Block the query if any inappropriate word is found
    return False


def wiki_summary(data: str)-> str:
    wiki_topic = "_".join(data.split())
    wiki_link = f"https://en.wikipedia.org/wiki/{wiki_topic}"
    wiki_response = requests.get(wiki_link)
    if wiki_response.status_code == 200:
        wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
        wiki_paragraphs = wiki_soup.select('.mw-parser-output p')
        wiki_text_content = [p.get_text() for p in wiki_paragraphs][:5]
        wiki_text_content = " ".join(wiki_text_content)
        wiki_out = ""
        for word in wiki_text_content.split():
            if not word.startswith("[") and not word.endswith("]"):
                if word.endswith("."):
                    wiki_out +=  word + "\n"
                else:
                    wiki_out += word + " "
    else:
        wiki_out = 'Failed to retrieve Wikipedia content'
    return wiki_out

# def chatgpt_res(data:str)->str:
#     question = f"Summarise topic {data} for me in 250 words.Give the best explanation you can."

#     response = client.chat.completions.create(
#         model = "gpt-3.5-turbo",
#         messages=[{"role" : "user", "content" : question}],
#         stream=True
#     )

#     output = ""
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             output += chunk.choices[0].delta.content
#     return output





def google_res(data:str)->str:
    google_url = f"https://www.google.com/search?q={data}"
    google_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    google_response = requests.get(google_url, headers=google_headers)
    if google_response.status_code == 200:
        google_soup = BeautifulSoup(google_response.text, 'html.parser')
        google_search_results = google_soup.find_all('div', class_='tF2Cxc')
        google_out = []
        for result in google_search_results:
            title = result.find('h3').text
            link = result.a['href']
            google_out.append((title, link))
    else:
        google_out = [("Failed to retrieve","search results from Google")]
    return google_out


def youtube_links(query, num_results=10):
    i = 0
    search_results = Search(query).results
    video_urls = []
    for result in search_results[:num_results]:
        video_id = result.video_id
        video_urls.append((video_id, i))
        i += 1
    
    return video_urls

def google_book_search(query):
    url = f"https://www.google.com/search?q={query}+site:books.google.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='tF2Cxc')
    print(response.status_code)
    books = []
    for result in search_results:
        title = result.find('h3').text
        link = result.a['href']
        books.append((title, link))
    for i, j in books:
        print(i, j)
    return books