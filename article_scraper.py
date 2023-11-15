import requests
from bs4 import BeautifulSoup


class ArticleScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def parse_article(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Extracting the title, author, and publication date
        title = soup.find("h1").text if soup.find("h1") else "No title found"
        author = (
            soup.find("meta", {"name": "author"})["content"]
            if soup.find("meta", {"name": "author"})
            else "No author found"
        )
        pub_date = (
            soup.find("meta", {"property": "article:published_time"})["content"]
            if soup.find("meta", {"property": "article:published_time"})
            else "No publication date found"
        )

        # Extracting the main content
        # Assuming main content is within <article> tag
        article_content = soup.find("article")
        if article_content:
            paragraphs = article_content.find_all("p")
            content = " ".join(paragraph.text for paragraph in paragraphs)
        else:
            content = "No content found"

        return {
            "title": title,
            "author": author,
            "publication_date": pub_date,
            "content": content,
        }

    def scrape_article(self):
        html = self.fetch_page()
        if html:
            return self.parse_article(html)


if __name__ == "__main__":
    url = (
        "https://medium.com/fively/best-tech-stack-for-web-app-development-4e81beb4cc2d"
    )
    scraper = ArticleScraper(url)
    article_data = scraper.scrape_article()
    print(article_data)
