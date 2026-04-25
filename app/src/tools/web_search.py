import httpx
from src.core.config import config
from src.contracts.tool_results import WebSearchResult


class TavilyWebSearcher:
    """Универсальный web search через Tavily.

    Агент сам формирует запрос — тул просто его выполняет.
    """

    async def search(self, query: str) -> WebSearchResult:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": config.tavily_api_key,
                    "query": query,
                    "max_results": 5,
                    "include_answer": True,
                },
            )
        resp.raise_for_status()
        data = resp.json()

        return {
            "query": query,
            "answer": data.get("answer", ""),
            "results": [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "content": r["content"][:400],
                }
                for r in data.get("results", [])[:4]
            ],
        }
