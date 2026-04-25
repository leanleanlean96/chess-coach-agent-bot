from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_ignore_empty=True,
        case_sensitive=False,
    )
    bot_token: str
    api_key: str
    llm_model: str
    base_url: str
    tavily_api_key: str
    youtube_api_key: str
    lichess_api_token: str


config = BotConfig()
