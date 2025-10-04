import json
import logging
from sqlalchemy.orm import Session
from app.repositories.connector_repository import ConnectorRepository
from app.repositories.connector_status_repository import ConnectorStatusRepository
from app.schemas.connectors_schema import ConnectorCreate, ConnectorOut
from app.schemas.connectors_status_schema import ConnectorStatusOut
from app.models.connector_status import ConnectorStatus
from app.redis import get_redis
from app.api.metrics import CONNECTORS_CREATED, CONNECTORS_DELETED, CONNECTORS_UPDATED

CACHE_KEY_CONNECTORS_LIST = "connectors:static"
CACHE_KEY_CONNECTOR = "connector:{id}"
CACHE_TTL = 3600

class ConnectorService:
    def __init__(self, db: Session):
        self.repo = ConnectorRepository(db)
        self.status_repo = ConnectorStatusRepository(db)
        self.redis = get_redis()


    def create_connector(self, connector_data: ConnectorCreate):
        connector = self.repo.create(connector_data)
        connector_out = ConnectorOut.from_orm(connector)

        self.redis.set(
            CACHE_KEY_CONNECTOR.format(id=connector.id),
            json.dumps(connector_out.model_dump()),
            ex=CACHE_TTL
        )

        cached = self.redis.get(CACHE_KEY_CONNECTORS_LIST)
        if cached:
            connectors_list = json.loads(cached)
        else:
            connectors_list = []

        connectors_list.append(connector_out.model_dump())
        self.redis.set(
            CACHE_KEY_CONNECTORS_LIST,
            json.dumps(connectors_list),
            ex=CACHE_TTL
        )
        CONNECTORS_CREATED.inc() 

        return connector
 
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
        CONNECTORS_UPDATED.inc()

        return connector 

    def get_connector(self, connector_id: int):
        cache_key = CACHE_KEY_CONNECTOR.format(id=connector_id)
        cached = self.redis.get(cache_key)

        if cached:
            logging.info(f"Cache hit for connector {connector_id}")
            return ConnectorOut(**json.loads(cached))
        
        logging.info(f"Cache miss for connector {connector_id}")
        logging.info(f"Retrieving from BD: {connector_id}")
        connector_db = self.repo.get(connector_id)
        if not connector_db:
            return None 

        connector_out = ConnectorOut.from_orm(connector_db)

        self.redis.set(
            cache_key,
            json.dumps(connector_out.model_dump()), 
            ex=CACHE_TTL
        )

        return connector_out

    def delete_connector(self, connector_id: int):
        success = self.repo.delete(connector_id)
        if not success:
            raise ValueError(f"Connector with id {connector_id} not found")

        logging.info(f"Deleting {connector_id} from independent cache")
        self.redis.delete(CACHE_KEY_CONNECTOR.format(id=connector_id))
        cached = self.redis.get(CACHE_KEY_CONNECTORS_LIST)

        if cached:
            connectors_list = json.loads(cached)
            logging.info(f"Deleting {connector_id} global connectors cache list")
            updated_list = [c for c in connectors_list if c["id"] != connector_id]
            self.redis.set(
                CACHE_KEY_CONNECTORS_LIST,
                json.dumps(updated_list),
                ex=CACHE_TTL
            )

        CONNECTORS_DELETED.inc()

        return success

 
    def list_connectors(self):
        cached = self.redis.get(CACHE_KEY_CONNECTORS_LIST)

        if cached:
            logging.info("Cache hit for connectors list")
            cached_list = json.loads(cached)
            return [ConnectorOut(**c) for c in cached_list]

        logging.info("Cache miss for connectors list")
        logging.info("Retrieving it from BD")
        connectors = self.repo.list_all()
        connectors_out = [ConnectorOut.from_orm(c) for c in connectors]

        self.redis.set(
            CACHE_KEY_CONNECTORS_LIST,
            json.dumps([c.model_dump() for c in connectors_out]),
            ex=CACHE_TTL
        )

        return connectors_out

    def list_by_charging_point(self, charging_point_id: int):
        return self.repo.list_by_charging_point(charging_point_id)


    def list_by_status(self, status_id: int):
        return self.repo.list_by_status(status_id)