from bs4 import BeautifulSoup
import requests
import re
import os
from datetime import datetime

def scrape_news():
    # Scraping functionality
    response = requests.get("https://www.animenewsnetwork.com")
    soup = BeautifulSoup(response.text, "html.parser")
    mainfeed = soup.find_all("div", class_="mainfeed-day")[1]
    titles = []
    links = []

    # Extract the date from the data-day attribute of mainfeed and convert to word format
    mainfeed_date_str = mainfeed.get("data-day")  # e.g., '2025-05-27'
    if mainfeed_date_str:
        mainfeed_date_obj = datetime.strptime(mainfeed_date_str, "%Y-%m-%d")
        mainfeed_date_in_words = mainfeed_date_obj.strftime("%B %d, %Y")
    else:
        mainfeed_date_in_words = "Unknown Date"


    articles = mainfeed.select('.herald-boxes .t-news .wrap div h3 a')
    for article in articles:
        titles.append(article.text)
        links.append(article['href'])

    content_by_title = {}

    def clean_text(text):
        # Remove multiple blank lines
        text = re.sub(r'\n\s*\n+', '\n', text)
        # Remove leading/trailing spaces on each line
        text = '\n'.join(line.strip() for line in text.splitlines())
        return text

    for idx in range(len(titles)):
        article_response = requests.get("https://www.animenewsnetwork.com" + links[idx])
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        content_div = article_soup.find("div", class_="meat")
        if content_div:
            article_text = "\n".join(content_div.stripped_strings)
            article_text = clean_text(article_text)
        else:
            article_text = ""
        content_by_title[titles[idx]] = article_text

    # Prepare newsletter content (without the date)
    newsletter_content = ""
    for title, content in content_by_title.items():
        newsletter_content += "### STORY START\n"
        newsletter_content += f"TITLE: {title}\n"
        newsletter_content += f"CONTENT: {content.strip()}\n"
        newsletter_content += "### STORY END\n\n"

    output_path = '/tmp/scraped_content.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Date: {mainfeed_date_in_words}\n\n")
        f.write(newsletter_content)

    print("Scraping completed. Results written to scraped_content.txt")
