WEB_SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Выполняет поиск в интернете по произвольному запросу. "
            "Используй для поиска лучших шахматных дебютов для рейтинга игрока, "
            "UCI-ходов конкретного дебюта, теоретических материалов. "
            "Формируй запрос на русском языке, конкретно и точно."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Поисковый запрос на русском. "
                        "Примеры: "
                        "'лучшие дебюты для белых рейтинг 900 шахматы', "
                        "'Итальянская партия ходы UCI нотация e2e4 e7e5'",
                    ),
                },
            },
            "required": ["query"],
        },
    },
}


GET_STATS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_opening_stats",
        "description": (
            "Получает реальную статистику дебюта из базы Lichess: "
            "процент побед белых/чёрных/ничьих, число партий, топ продолжения. "
            "Требует UCI-ходы дебюта — получай их через web_search, не придумывай."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "opening_name": {
                    "type": "string",
                    "description": "Название дебюта (например, 'Итальянская партия')",
                },
                "moves": {
                    "type": "string",
                    "description": (
                        "Ходы дебюта в UCI-нотации через запятую "
                        "(например, 'e2e4,e7e5,g1f3,b1c3,f1c4'). "
                        "Получай через web_search — не придумывай."
                    ),
                },
            },
            "required": ["opening_name", "moves"],
        },
    },
}


FIND_VIDEO_SCHEMA = {
    "type": "function",
    "function": {
        "name": "find_video",
        "description": (
            "Ищет видео на YouTube. "
            "Для поиска последних/новых видео используй order='date'. "
            "Для поиска лучших обучающих видео используй order='relevance'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Поисковый запрос на русском или английском",
                },
                "order": {
                    "type": "string",
                    "enum": ["relevance", "date"],
                    "description": (
                        "Сортировка: relevance — по релевантности (по умолчанию), "
                        "date — по дате загрузки (для поиска последних видео)"
                    ),
                },
            },
            "required": ["query"],
        },
    },
}
