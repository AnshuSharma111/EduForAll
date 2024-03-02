import requests
from bs4 import BeautifulSoup

def wiki_summary(data: str)-> str:
    wiki_topic = "_".join(data.split())
    wiki_link = f"https://en.wikipedia.org/wiki/{wiki_topic}"
    wiki_response = requests.get(wiki_link)
    if wiki_response.status_code == 200:
        wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
        wiki_paragraphs = wiki_soup.select('.mw-parser-output p')
        wiki_text_content = [p.get_text() for p in wiki_paragraphs][:10]
        wiki_text_content = " ".join(wiki_text_content)
        wiki_out = ""
        for word in wiki_text_content.split():
            if not word.startswith("[") and not word.endswith("]"):
                if word.endswith("."):
                    wiki_out += ".\n"
                else:
                    wiki_out += word + " "
    else:
        wiki_out = 'Failed to retrieve Wikipedia content'
    return wiki_out

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
        out = ""
        for result in google_search_results:
            title = result.find('h3').text
            link = result.a['href']
            google_out.append((title, link))
        for title, link in google_out:
            out += "Title: " + title + "\nLink: " + link + "\n\n"
    else:
        out = "Failed to retrieve search results from Google"
    return out