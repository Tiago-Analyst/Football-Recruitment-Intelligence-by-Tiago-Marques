"""Club-oriented query service."""
from src.data.repositories import AnalyticsRepository


class ClubService:
    """Expose club analysis from the warehouse."""

    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def clubs(self):
        return self.repository.query(
            "SELECT club_key, club_name FROM dim_clubs WHERE domestic_competition_id='PO1' ORDER BY club_name"
        )

