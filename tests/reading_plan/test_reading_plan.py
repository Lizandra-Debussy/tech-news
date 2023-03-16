from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501

from unittest.mock import patch
import pytest


mock_news = [
    {
        "url": "https://www.example.com/news1",
        "title": "Notícia bacana",
        "timestamp": "2022-03-01T10:00:00Z",
        "writer": "Autor 1",
    },
    {
        "url": "https://www.example.com/news2",
        "title": "Notícia bacana 2",
        "timestamp": "2022-03-01T11:00:00Z",
        "writer": "Autor 2",
    },
]


def test_reading_plan_group_news():
    readingPlan = ReadingPlanService()

    # Define o valor esperado para available_time = 5
    expected = {
        "readable": [
            {
                "unfilled_time": 1,
                "chosen_news": [
                    ("Notícia bacana", 4),
                ],
            },
            {
                "unfilled_time": 4,
                "chosen_news": [
                    ("Notícia bacana 2", 1),
                ],
            },
        ],
        "unreadable": [],
    }

    with patch("tech_news.database.find_news") as mock_find_news:
        # Define o retorno da função mockada
        mock_find_news.return_value = mock_news

        assert readingPlan.group_news_for_available_time(5) == expected

    # Testa se ValueError é lançado quando available_time é menor ou igual a 0
    with pytest.raises(ValueError) as info:
        readingPlan.group_news_for_available_time(0)
    assert str(info.value) == "Valor 'available_time' deve ser maior que zero"

    # expected2 = {
    #     "readable": [
    #         {
    #             "unfilled_time": 5,
    #             "chosen_news": [
    #                 ("Notícia bacana", 4),
    #                 ("Notícia bacana 2", 1),
    #             ],
    #         },
    #     ],
    #     "unreadable": [("Notícia 3", 15)],
    # }

    # with patch("tech_news.database.find_news") as mock_find_news:
    #     mock_find_news.return_value = mock_news

    #     assert readingPlan.group_news_for_available_time(10) == expected2
