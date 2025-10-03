from sqlalchemy.orm import Session
from app.repositories.charging_point_repository import ChargingPointRepository
from app.schemas.charging_points_schema import ChargingPointCreate


class ChargingPointService:
    def __init__(self, db: Session):
        self.repo = ChargingPointRepository(db)

  
    def create_charging_point(self, cp_data: ChargingPointCreate):
        return self.repo.create(cp_data)


    def list_all(self):
        return self.repo.list_all()

    def get_charging_point(self, cp_id: int):
        return self.repo.get(cp_id)


    def delete_charging_point(self, cp_id: int):
        success = self.repo.delete(cp_id)
        if not success:
            raise ValueError(f"ChargingPoint with id {cp_id} not found")
        return success


    def list_by_station(self, station_id: int):
        return self.repo.list_by_station(station_id)