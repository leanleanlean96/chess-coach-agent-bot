import httpx
from src.core.config import config
from src.contracts.tool_results import VideoSearchResult


class YouTubeVideoFinder:

    async def find(self, query: str, order: str = "relevance") -> VideoSearchResult:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "key": config.youtube_api_key,
                    "q": query,
                    "part": "snippet",
                    "type": "video",
                    "maxResults": 3,
                    "order": order,
                    "relevanceLanguage": "ru",
                    "regionCode": "RU",
                    "videoDuration": "medium",
                },
            )

        if resp.status_code != 200:
            return {
                "query": query,
                "videos": [],
                "error": f"YouTube API недоступен (status {resp.status_code})",
            }

        videos = []
        for item in resp.json().get("items", []):
            vid_id = item["id"]["videoId"]
            snippet = item["snippet"]
            videos.append(
                {
                    "title": snippet["title"],
                    "channel": snippet["channelTitle"],
                    "url": f"https://youtube.com/watch?v={vid_id}",
                }
            )

        return {
            "query": query,
            "videos": videos,
        }
