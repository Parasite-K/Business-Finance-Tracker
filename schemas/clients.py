from pydantic import BaseModel

from schemas.projects import ProjectsResponse

class ClientsCreate(BaseModel):
    name: str
    gstin: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None

class ClientsResponse(BaseModel):
    id: int
    name: str
    gstin: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None

class ClientsUpdate(BaseModel):
    name: str
    gstin: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None

class ClientProjectsResponse(BaseModel):
    client_id: int
    client_name: str
    gstin: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    projects: list[ProjectsResponse]