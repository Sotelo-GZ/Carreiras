from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Carreiras API"
    database_url: str = "sqlite:///./carreiras.db"
    scrape_source_url: str = "https://www.carreirasgalegas.com/events"
    geocode_url: str = "https://nominatim.openstreetmap.org/search"
    geocode_user_agent: str = "carreiras-app/1.0"
    scrape_timeout_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
