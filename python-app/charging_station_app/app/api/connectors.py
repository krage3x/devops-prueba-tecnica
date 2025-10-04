from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.connectors_schema import ConnectorOut, ConnectorCreate, ConnectorUpdateStatus
from app.services.connector_service import ConnectorService
from app.database import get_db


router = APIRouter(prefix="/connectors", tags=["connectors"])

@router.get("/", response_model=List[ConnectorOut])
def list_connectors(db: Session = Depends(get_db)):
    service = ConnectorService(db)
    return service.list_connectors()

@router.get("/{connector_id}", response_model=ConnectorOut)
def get_connector(connector_id: int, db: Session = Depends(get_db)):
    service = ConnectorService(db)
    connector = service.get_connector(connector_id)
    if not connector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connector with id {connector_id} not found"
        )
    return connector


@router.post("/", response_model=ConnectorOut, status_code=status.HTTP_201_CREATED)
def create_connector(connector_data: ConnectorCreate, db: Session = Depends(get_db)):
    service = ConnectorService(db)
    return service.create_connector(connector_data)


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connector(connector_id: int, db: Session = Depends(get_db)):
    service = ConnectorService(db)
    try:
        service.delete_connector(connector_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{connector_id}/update-status", response_model=ConnectorOut)
def update_connector_status(
    connector_id: int,
    status_update: ConnectorUpdateStatus,
    db: Session = Depends(get_db)
):
    service = ConnectorService(db)
    try:
        updated_connector = service.update_connector_status(
            connector_id, status_update.status_name
        )
        return updated_connector
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))