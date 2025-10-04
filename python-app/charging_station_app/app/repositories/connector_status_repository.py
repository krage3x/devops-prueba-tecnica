from sqlalchemy.orm import Session
from app.models.connector_status import ConnectorStatus
from app.schemas.connectors_status_schema import ConnectorStatusCreate


class ConnectorStatusRepository:
    def __init__(self, db_session: Session):
        self.db = db_session


    def get(self, status_id: int) -> ConnectorStatus | None:
        return self.db.query(ConnectorStatus).filter(ConnectorStatus.id == status_id).first()

    def get_by_name(self, name: str) -> ConnectorStatus | None:
        return (
            self.db.query(ConnectorStatus)
            .filter(ConnectorStatus.name == name)
            .first()
        )

    def list_all(self) -> list[ConnectorStatus]:
        return self.db.query(ConnectorStatus).all()