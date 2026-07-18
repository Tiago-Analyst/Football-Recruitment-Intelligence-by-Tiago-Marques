"""Player-oriented query service."""
from src.data.repositories import AnalyticsRepository


class PlayerService:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def profile(self, player_key: int):
        return self.repository.query("SELECT * FROM dim_players WHERE player_key=?", [player_key])

