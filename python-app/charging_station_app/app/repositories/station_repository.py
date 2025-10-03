from sqlalchemy.orm import Session
from app.models.station import Station
from app.schemas.stations_schema import StationCreate


class StationRepository:
    def __init__(self, db_session: Session):
        self.db = db_session


    def create(self, station_data: StationCreate) -> Station:
        new_station = Station(
            name=station_data.name,
            location=station_data.location,
        )
        self.db.add(new_station)
        self.db.commit()
        self.db.refresh(new_station)
        return new_station

    def get(self, station_id: int) -> Station | None:
        return self.db.query(Station).filter(Station.id == station_id).first()


    def delete(self, station_id: int) -> bool:
        station = self.get(station_id)
        if not station:
            return False
        self.db.delete(station)
        self.db.commit()
        return True

    def list_all(self) -> list[Station]:
        return self.db.query(Station).all()