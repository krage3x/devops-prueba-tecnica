from sqlalchemy.orm import Session
from app.repositories.connector_repository import ConnectorRepository
from app.repositories.connector_status_repository import ConnectorStatusRepository
from app.schemas.connectors_schema import ConnectorCreate
from app.models.connector_status import ConnectorStatus


class ConnectorService:
    def __init__(self, db: Session):
        self.repo = ConnectorRepository(db)
        self.status_repo = ConnectorStatusRepository(db)


    def create_connector(self, connector_data: ConnectorCreate):
        return self.repo.create(connector_data)
 
    def update_connector_status(self, connector_id: int, status_name: str):
        connector = self.repo.get(connector_id)
        if not connector:
            raise ValueError(f"Connector with id {connector_id} not found")
        status = self.status_repo.get_by_name(status_name)
        if not status:
            raise ValueError(f"ConnectorStatus '{status_name}' not found")

        connector.status_id = status.id
        connector.status = status

        self.repo.update(connector)

        return connector 

    def get_connector(self, connector_id: int):
        return self.repo.get(connector_id)


    def delete_connector(self, connector_id: int):
        success = self.repo.delete(connector_id)
        if not success:
            raise ValueError(f"Connector with id {connector_id} not found")
        return success

 
    def list_connectors(self):
        return self.repo.list_all()

   
    def list_by_charging_point(self, charging_point_id: int):
        return self.repo.list_by_charging_point(charging_point_id)


    def list_by_status(self, status_id: int):
        return self.repo.list_by_status(status_id)