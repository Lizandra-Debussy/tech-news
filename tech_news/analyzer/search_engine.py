from tech_news.database import search_news


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": f".*{title}.*", "$options": "i"}}
    search_news_db = search_news(query)
    result = []

    for new in search_news_db:
        result.append((new["title"], new["url"]))

    return result


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
