from sqlalchemy.orm import Session
from app.models.connector import Connector
from app.schemas.connectors_schema import ConnectorCreate, ConnectorUpdateStatus


class ConnectorRepository:
    def __init__(self, db_session: Session):
        self.db = db_session


    def create(self, connector_data: ConnectorCreate) -> Connector:
        new_connector = Connector(
            type=connector_data.type,
            charging_point_id=connector_data.charging_point_id,
            status_id=connector_data.status_id
        )
        self.db.add(new_connector)
        self.db.commit()
        self.db.refresh(new_connector)
        return new_connector

    def update(self, connector_update: ConnectorUpdateStatus) -> Connector:
        connector_id = connector_update.id

        connector = self.db.query(Connector).filter(Connector.id == connector_id).first()
        if not connector:
            raise Exception(f"Connector with id {connector_id} not found")

        self.db.commit()       
        self.db.refresh(connector)
        return connector


    def get(self, connector_id: int) -> Connector | None:
        return self.db.query(Connector).filter(Connector.id == connector_id).first()

    def delete(self, connector_id: int) -> bool:
        connector = self.get(connector_id)
        if not connector:
            return False
        self.db.delete(connector)
        self.db.commit()
        return True

    def list_all_static_fields(self):
        return self.db.query(
            Connector.id,
            Connector.type,
            Connector.charging_point_id
        ).all()

    def list_all(self) -> list[Connector]:
        return self.db.query(Connector).all()