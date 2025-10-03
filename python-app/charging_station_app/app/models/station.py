from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from app.database import DB_SCHEMA
from app.models.base import Base

stations_id_seq = Sequence("stations_id_seq", schema=DB_SCHEMA)



class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, stations_id_seq, primary_key=True, index=True)
    name = Column(String, nullable=False)            
    location = Column(String, nullable=False)        

    charging_points = relationship("ChargingPoint", back_populates="station", lazy="select",cascade="all, delete-orphan")
