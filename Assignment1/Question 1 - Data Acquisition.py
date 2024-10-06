import requests
from bs4 import BeautifulSoup
import csv
import json
import re
def is_valid_bbc_link(link):
    pattern = r'^/news\/articles\/[a-zA-Z0-9]+$'
    return re.match(pattern, link) is not None
def scrape_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_data = []
    for article in soup.find_all("a", href=True):
        title = article.get_text(strip=True)
        link = article['href']
        # print(is_valid_bbc_link(link))
        if is_valid_bbc_link(link):
            if not link.startswith("https"):
                link = "https://www.bbc.com" + link
            if title and link:
                news_data.append((title, link))
        else:
            pass
    return news_data

def save_csv(data, filename='news_data.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])
        for row in data:
            writer.writerow(row)
def save_json(data, filename='news_data.json'):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    news_data = scrape_news()
    save_csv(news_data)
    news_data_dict = [{"title": title, "link": link} for title, link in news_data]
    save_json(news_data_dict)



