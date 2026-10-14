from fastapi import APIRouter, HTTPException
from psycopg.errors import ForeignKeyViolation


from storage import (
    load_clients,
    save_client,
    update_client,
    delete_client,
    load_one_client,
    load_client_with_projects
)
from schemas.clients import (
    ClientsCreate,
    ClientsResponse,
    ClientsUpdate,
    ClientProjectsResponse
)

router = APIRouter()

@router.post("/clients")
def create_client(client: ClientsCreate):
    client_id = save_client(
        client.name,
        client.gstin,
        client.address,
        client.phone,
        client.email
    )

    return {
        "message": "Client successfully created.",
        "client_id": client_id
    }



@router.get("/clients", response_model=list[ClientsResponse])
def get_clients():
    return load_clients()

@router.get("/clients/{client_id}", response_model=ClientsResponse)
def get_one_client(client_id: int):
    client = load_one_client(client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    return client



@router.put("/clients/{client_id}", response_model=ClientsResponse)
def edit_project(client_id: int, client: ClientsUpdate):
    updated = update_client(
        client.name,
        client.gstin,
        client.address,
        client.phone,
        client.email,
        client_id     
    )

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail="Client Not Found"
        )
    
    return load_one_client(client_id)


@router.delete("/clients/{client_id}")   
def del_client(client_id: int):
    try:
        deleted = delete_client(client_id)
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this client because it has associated projects."
        )

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Client Not Found."
        )

    return {
        "message": "Client deleted successfully",
        "project_id": client_id
    }


@router.get("/clients/{client_id}/projects", response_model=ClientProjectsResponse)
def get_client_with_projects(client_id: int):
    rows = load_client_with_projects(client_id)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Client not found."
        )
    projects = []

    for row in rows:
        if row["project_id"] is not None:
            project = {
                "id": row["project_id"],
                "name": row["project_name"],
                "client_id": row["client_id"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "estimated_revenue": row["estimated_revenue"]
            }
            projects.append(project)

        

    client = {
        "client_id": rows[0]["client_id"],
        "client_name": rows[0]["client_name"],
        "gstin": rows[0]["gstin"],
        "address": rows[0]["address"],
        "phone": rows[0]["phone"],
        "email": rows[0]["email"],
        "projects": projects
        }

    return client