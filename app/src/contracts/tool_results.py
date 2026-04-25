from typing import TypedDict, Protocol


class SearchResult(TypedDict):
    title: str
    url: str
    content: str


class WebSearchResult(TypedDict):
    query: str
    answer: str
    results: list[SearchResult]


class ContinuationInfo(TypedDict):
    move: str
    games: int
    white_wins_pct: float


class OpeningStatsResult(TypedDict):
    opening: str
    moves: str
    total_games: int
    white_wins_pct: float
    draws_pct: float
    black_wins_pct: float
    top_continuations: list[ContinuationInfo]
    source: str


class VideoInfo(TypedDict):
    title: str
    channel: str
    url: str


class VideoSearchResult(TypedDict):
    query: str
    videos: list[VideoInfo]


class WebSearcher(Protocol):
    """Web search interface"""

    async def search(self, query: str) -> WebSearchResult: ...


class OpeningStatsProvider(Protocol):
    """Chess Opening stats provider"""

    async def get_stats(self, opening_name: str, moves: str) -> OpeningStatsResult: ...


class VideoFinder(Protocol):
    """Video search engine interface"""

    async def find(self, query: str) -> VideoSearchResult: ...
