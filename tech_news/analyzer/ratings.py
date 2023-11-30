from tech_news.database import search_news
from collections import Counter


# Requisito 10
def top_5_categories():
    all_news = search_news({})

    all_categories = []
    for news in all_news:
        category = news.get("category")
        if category:
            all_categories.append(category)

    categories_count = Counter(all_categories)

    # Ordenar as categorias por popularidade e em ordem alfabética
    sorted_categories = sorted(
        categories_count.items(),
        # Ordenar por contagem decrescente e depois por ordem alfabética
        key=lambda x: (-x[1], x[0])
    )

    # Retornar as cinco categorias mais populares ou menos se houver menos de 5
    top_categories = []
    for category, _ in sorted_categories[:5]:
        top_categories.append(category)

    return top_categories
