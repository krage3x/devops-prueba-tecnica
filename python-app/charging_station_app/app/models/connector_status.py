# app/models/connector_status.py
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.database import DB_SCHEMA

connector_status_id_seq = Sequence("connector_status_id_seq", schema=DB_SCHEMA)


class ConnectorStatus(Base):
    __tablename__ = "connector_status"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, connector_status_id_seq, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    connectors = relationship("Connector", back_populates="status",lazy="select")