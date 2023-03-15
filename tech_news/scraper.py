import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)

    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    news_links = []
    selector = Selector(text=html_content)
    articles = selector.css(".entry-preview")

    for article in articles:
        link = article.css("h2.entry-title a::attr(href)").get()
        news_links.append(link)

    return news_links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_link = selector.css(".next.page-numbers::attr(href)").get()

    if next_page_link:
        return next_page_link
    return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    news_dict = {}

    news_dict["url"] = (
        selector.css('link[rel="canonical"]::attr(href)').get().strip()
    )
    news_dict["title"] = selector.css("h1.entry-title::text").get().strip()

    news_dict["timestamp"] = selector.css("li.meta-date::text").get().strip()

    news_dict["writer"] = (
        selector.css("li.meta-author span.author a::text").get().strip()
    )

    news_dict["reading_time"] = int(
        selector.css("li.meta-reading-time::text").re_first(r"\d+")
    )

    # news_dict["summary"] = (
    #     selector.css("div.entry-content p:nth-child(2)::text")[0].get()
    # .strip()
    # )

    # news_dict["summary"] = (
    #     selector.css("div.entry-content p *::text")[0].get().strip()
    # ) <<<< ====

    # deu certo no teste manual mas não passou no avaliador
    # p = ' '.join(
    #     selector.css("div.entry-content > p:first-child::text").extract())
    # news_dict["summary"] = p

    summary = "".join(
        selector.css("div.entry-content > p:nth-of-type(1) *::text").extract()
    )
    news_dict["summary"] = summary.strip()

    news_dict["category"] = (
        selector.css(".category-style span.label::text").get().strip()
    )

    return news_dict


# Requisito 5
def get_tech_news(amount):
    page_link = "https://blog.betrybe.com/"
    news_list = []

    while len(news_list) < amount and page_link:
        page_content = fetch(page_link)
        news_links = scrape_updates(page_content)
        for link in news_links:
            html_content = fetch(link)
            news_dict = scrape_news(html_content)

            news_list.append(news_dict)
            if len(news_list) == amount:
                break

        page_link = scrape_next_page_link(page_content)

    create_news(news_list)
    return news_list

# html = fetch("https://blog.betrybe.com/tecnologia/arquivo-bin/")
# news_dict = scrape_news(html)
# print(get_tech_news(2))
