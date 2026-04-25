from collections import defaultdict
import json
from pathlib import Path
from openai import AsyncOpenAI

from src.contracts.tool_results import WebSearcher, OpeningStatsProvider, VideoFinder
from src.core.config import config
from src.agent.schemas import WEB_SEARCH_SCHEMA, GET_STATS_SCHEMA, FIND_VIDEO_SCHEMA
from src.agent.prompts import SYSTEM_PROMPT

TOOLS = [WEB_SEARCH_SCHEMA, GET_STATS_SCHEMA, FIND_VIDEO_SCHEMA]

client = AsyncOpenAI(
    api_key=config.api_key,
    base_url=config.base_url,
)

_histories: dict[int, list] = defaultdict(list)


async def process_message(
    user_text: str,
    chat_id: int,
    searcher: WebSearcher,
    stats: OpeningStatsProvider,
    finder: VideoFinder,
) -> str:
    tool_map = {
        "web_search": lambda a: searcher.search(**a),
        "get_opening_stats": lambda a: stats.get_stats(**a),
        "find_video": lambda a: finder.find(**a),
    }

    history = _histories[chat_id]
    if not history:
        history.append({"role": "system", "content": SYSTEM_PROMPT})
    history.append({"role": "user", "content": user_text})

    for _ in range(10):
        response = await client.chat.completions.create(
            model=config.llm_model,
            messages=history,
            tools=TOOLS,
            temperature=0.3,
            max_tokens=1500,
        )

        msg = response.choices[0].message
        assistant_msg = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant_msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        history.append(assistant_msg)

        if not msg.tool_calls:
            _histories[chat_id] = history
            return msg.content or "Не удалось сформировать ответ."

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = (
                    await tool_map[name](args)
                    if name in tool_map
                    else {"error": f"Неизвестный инструмент: {name}"}
                )
            except Exception as e:
                result = {"error": f"Инструмент недоступен: {str(e)}"}

            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

    _histories[chat_id] = history
    return "Превышен лимит итераций. Попробуй переформулировать вопрос."


def clear_history(chat_id: int) -> None:
    _histories.pop(chat_id, None)