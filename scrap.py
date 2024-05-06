import requests
from bs4 import BeautifulSoup
import json


def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    quotes = []
    authors = {}

    page_num = 1
    while True:
        url = f"{base_url}/page/{page_num}/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if "No quotes found!" in soup.text:
            break

        quote_elements = soup.find_all("div", class_="quote")
        for quote_element in quote_elements:
            quote_text = quote_element.find("span", class_="text").text
            author_name = quote_element.find("small", class_="author").text
            tags = [tag.text for tag in quote_element.find_all("a", class_="tag")]

            quotes.append({"quote": quote_text, "author": author_name, "tags": tags})

            if author_name not in authors:
                author_url = base_url + quote_element.find("a")["href"]
                authors[author_name] = {"author": author_name, "author_url": author_url}

        page_num += 1

    return quotes, list(authors.values())


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    quotes, authors = scrape_quotes()

    save_to_json(quotes, "quotes.json")

    save_to_json(authors, "authors.json")
