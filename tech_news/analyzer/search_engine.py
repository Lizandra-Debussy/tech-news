from tech_news.database import search_news
from datetime import datetime


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
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")

    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": formatted_date}
    search_news_db = search_news(query)
    result = []

    for news in search_news_db:
        result.append((news["title"], news["url"]))
    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
