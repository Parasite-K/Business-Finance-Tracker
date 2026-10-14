from fastapi import APIRouter, HTTPException
from psycopg.errors import ForeignKeyViolation


from storage import (
    load_projects,
    load_one_project,
    save_project,
    delete_project,
    update_project,
    get_project_stats,
)
from schemas.projects import (
    ProjectsCreate,
    ProjectsResponse,
    ProjectFinanceReports,
    ProjectsUpdate
)

router = APIRouter()


@router.get("/projects", response_model=list[ProjectsResponse])
def get_projects():
    return load_projects()


@router.get("/projects/{project_id}", response_model=ProjectsResponse)
def get_one_project(project_id: int):
    project = load_one_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project


@router.post("/projects")
def create_project(project: ProjectsCreate):
    project_id = save_project(
        project.name,
        project.client_id,
        project.start_date,
        project.end_date,
        project.estimated_revenue
        )

    return {
        "message": "Project successfully created.",
        "project_id": project_id
    }

@router.delete("/projects/{project_id}")   
def del_project(project_id: int):
    try:
        deleted = delete_project(project_id)
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this project because it has associated transactions."
        )

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Project Not Found."
        )

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }


@router.put("/projects/{project_id}", response_model=ProjectsResponse)
def edit_project(project_id: int, project: ProjectsUpdate):
    updated = update_project(
        project.name,
        project.client_id,
        project.start_date,
        project.end_date,
        project.estimated_revenue,
        project_id
    )

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail="Project Not Found"
        )
    
    return load_one_project(project_id)


@router.get("/projects/{project_id}/summary", response_model=ProjectFinanceReports)
def get_project_summary(project_id: int):

    stats = get_project_stats(project_id)

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail="Project Not Found"
        )

    return {
        "project_id": stats["project_id"],
        "transaction_count": stats["transaction_count"],
        "total_income": stats["income"],
        "total_expense": stats["expense"],
        "profit": stats["income"] - stats["expense"]
    }