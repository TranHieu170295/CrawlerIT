from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def scrapedata1(url1):
    response = requests.get(url1)
    soup = BeautifulSoup(response.content, "html.parser")

    conferences = []

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
    return conferences
def scrapedata2(url2):
    response = requests.get(url2)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Tạo một danh sách trống để lưu trữ thông tin đã in ra
    conferences = []
    # Tìm tất cả các thẻ <li> chứa thông tin về hội nghị
    for table in soup.find_all('table'):
        for row in table.find_all('tr', class_='row-2 even'):

            time_info = row.find('strong').get_text()
            location_info = row.find('td').get_text().split(':')[1][1:].split('[')[0]
            conference_name = row.find('a').get_text()
            conference_link = row.find('a')['href']
            conferences.append({
                'time': time_info,
                'name': conference_name,
                'location': location_info,
                'link': conference_link
            })
    return conferences
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_type = request.form['url_type']
        url_data = request.form['url']
        if url_type == 'url1':
            conferences_data = scrapedata1(url_data)
        elif url_type == 'url2':
            conferences_data = scrapedata2(url_data)
        return render_template('index.html', conferences=conferences_data)
    return render_template('index.html', conferences=None)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)