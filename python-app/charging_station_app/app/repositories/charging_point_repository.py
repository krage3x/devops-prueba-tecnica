from sqlalchemy.orm import Session
from app.models.charging_point import ChargingPoint
from app.schemas.charging_points_schema import ChargingPointCreate


class ChargingPointRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

  
    def create(self, cp_data: ChargingPointCreate) -> ChargingPoint:
        new_cp = ChargingPoint(
            code=cp_data.code,
            max_power_kw=cp_data.max_power_kw,
            station_id=cp_data.station_id
        )
        self.db.add(new_cp)
        self.db.commit()
        self.db.refresh(new_cp)
        return new_cp

  
    def get(self, cp_id: int) -> ChargingPoint | None:
        return self.db.query(ChargingPoint).filter(ChargingPoint.id == cp_id).first()


    def delete(self, cp_id: int) -> bool:
        cp = self.get(cp_id)
        if not cp:
            return False
        self.db.delete(cp)
        self.db.commit()
        return True


    def list_all(self) -> list[ChargingPoint]:
        return self.db.query(ChargingPoint).all()