from sqlalchemy.orm import Session
from app.repositories.station_repository import StationRepository
from app.schemas.stations_schema import StationCreate


class StationService:
    def __init__(self, db: Session):
        self.repo = StationRepository(db)


    def create_station(self, station_data: StationCreate):
        return self.repo.create(station_data)

    def list_stations(self):
        return self.repo.list_all()

    def get_station(self, station_id: int):
        return self.repo.get(station_id)

    def delete_station(self, station_id: int):
        success = self.repo.delete(station_id)
        if not success:
            raise ValueError(f"Station with id {station_id} not found")
        return success
