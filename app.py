from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

app = Flask(__name__)

def scrapedata(url):
    conferences = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        conference_list = soup.find("div", {"id": "eventList"}).find_all("li")

        for item in conference_list:
            if len(item.contents) > 1:
                time_info = item.contents[0].strip()
                conference_name = item.find("a").text.strip()
                location_info = item.contents[-1].strip()
                conference_link = item.find("a").get("href")

                conferences.append({
                    'time': time_info,
                    'name': conference_name,
                    'location': location_info,
                    'link': conference_link
                })
        pagination = soup.find("ul", class_="pagination")
        if pagination:
            next_page = pagination.find("a", rel="next")
            if next_page:
                url = urljoin(url, next_page.get("href"))
            else:
                url = None
        else:
            url = None
    return conferences

@app.route('/', methods=['GET', 'POST'])
def index():
    conferences_data = None
    if request.method == 'POST':
        url = request.form['url']
        conferences_data = scrapedata(url)
    return render_template('index.html', conferences=conferences_data)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)
