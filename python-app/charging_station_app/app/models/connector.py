from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from app.database import DB_SCHEMA
from app.models.base import Base

# Secuencia específica para la tabla connectors
connectors_id_seq = Sequence("connectors_id_seq", schema=DB_SCHEMA)


class Connector(Base):
    __tablename__ = "connectors"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, connectors_id_seq, primary_key=True, index=True)
    type = Column(String, nullable=False)             
    
    charging_point_id = Column(
        Integer, ForeignKey(f"{DB_SCHEMA}.charging_points.id"), nullable=False
    )
    charging_point = relationship("ChargingPoint", back_populates="connectors",lazy="select")

    
    status_id = Column(
        Integer, ForeignKey(f"{DB_SCHEMA}.connector_status.id"), nullable=False
    )
    status = relationship("ConnectorStatus", back_populates="connectors",lazy="select")