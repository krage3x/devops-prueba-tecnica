from pydantic import BaseModel

class ConnectorStatusCreate(BaseModel):
    name: str

class ConnectorStatusOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}