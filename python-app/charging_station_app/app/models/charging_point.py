from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from app.database import DB_SCHEMA
from app.models.base import Base

charging_points_id_seq = Sequence("charging_points_id_seq", schema=DB_SCHEMA)


class ChargingPoint(Base):
    __tablename__ = "charging_points"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, charging_points_id_seq, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)  
    max_power_kw = Column(Integer, nullable=False)      

    station_id = Column(Integer, ForeignKey(f"{DB_SCHEMA}.stations.id"), nullable=False)
    station = relationship("Station", back_populates="charging_points", lazy="select")

    connectors = relationship("Connector", back_populates="charging_point",lazy="select",cascade="all, delete-orphan")