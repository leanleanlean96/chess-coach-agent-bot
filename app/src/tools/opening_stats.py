import httpx
from src.core.config import config
from src.contracts.tool_results import OpeningStatsResult


class LichessStatsProvider:
    """Collects stats from lichess"""

    async def get_stats(self, opening_name: str, moves: str) -> OpeningStatsResult:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://explorer.lichess.ovh/lichess",
                headers={"Authorization": f"Bearer {config.lichess_api_token}"},
                params={
                    "variant": "standard",
                    "speeds": "blitz,rapid,classical",
                    "ratings": "1000,1200,1400,1600",
                    "play": moves,
                },
            )

        if resp.status_code != 200:
            return {
                "opening": opening_name,
                "moves": moves,
                "error": f"Lichess API недоступен (status {resp.status_code})",
            }

        data = resp.json()
        total = data.get("white", 0) + data.get("draws", 0) + data.get("black", 0)

        if total == 0:
            return {
                "opening": opening_name,
                "moves": moves,
                "error": "Недостаточно партий для статистики по этим ходам",
            }

        top_continuations = []
        for move in data.get("moves", [])[:3]:
            m_total = move["white"] + move["draws"] + move["black"]
            if m_total == 0:
                continue
            top_continuations.append(
                {
                    "move": move["san"],
                    "games": m_total,
                    "white_wins_pct": round(move["white"] / m_total * 100, 1),
                }
            )

        return {
            "opening": opening_name,
            "moves": moves,
            "total_games": total,
            "white_wins_pct": round(data["white"] / total * 100, 1),
            "draws_pct": round(data["draws"] / total * 100, 1),
            "black_wins_pct": round(data["black"] / total * 100, 1),
            "top_continuations": top_continuations,
            "source": "Lichess Opening Explorer, партии рейтинга 1000-1600",
        }
