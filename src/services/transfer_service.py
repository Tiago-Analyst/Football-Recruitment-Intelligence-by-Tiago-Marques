"""Transfer-oriented query service."""
from src.data.repositories import AnalyticsRepository


class TransferService:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def recent(self, limit: int = 100):
        return self.repository.query(
            "SELECT * FROM clean_transfers WHERE transfer_date<=CURRENT_DATE ORDER BY transfer_date DESC LIMIT ?",
            [limit],
        )
