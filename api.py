from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import (
    BaseModel,
    Field, 
    model_validator
)

from storage import (
    load_transactions, 
    save_transaction,
    load_one_transaction,
    delete_transaction,
    update_transaction,
    load_projects,
    load_one_project,
    save_project,
    delete_project,
    update_project,
    get_project_stats
)

from datetime import date
from data import categories


app = FastAPI()

class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float = Field(ge=0)
    project_id: int | None = None

    @model_validator(mode="after")
    def validate_category(self):
        if self.category not in categories[self.type]:
            raise ValueError("Category does not match transaction type.")

        return self

class TransactionResponse(BaseModel):
    id: int
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float
    project_id: int | None


class TransactionUpdate(BaseModel):
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float = Field(ge=0)
    project_id: int | None = None

    @model_validator(mode="after")
    def validate_category(self):
        if self.category not in categories[self.type]:
            raise ValueError("Category does not match transaction type.")

        return self
    


@app.get("/")
def home():
    return {"message": "Business Finance Tracker API"}

@app.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    txn_id = save_transaction(
        transaction.type,
        transaction.category,
        transaction.description,
        transaction.date,
        transaction.amount,
        transaction.project_id    #HANDLE PROJECT ID DOES NOT EXIST!!!!!!!
    )
    return {
        "message": "Transaction created successfully",
        "transaction_id": txn_id
    }




@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions():
    return load_transactions()

@app.get("/transactions/{txn_id}", response_model=TransactionResponse)
def get_one_transaction(txn_id: int):
    transaction =  load_one_transaction(txn_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction

@app.delete("/transactions/{txn_id}")
def del_transaction(txn_id: int):
    deleted = delete_transaction(txn_id)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )

    return {
        "message": "Transaction deleted successfully",
        "transaction_id": txn_id
    }

@app.put("/transactions/{txn_id}", response_model=TransactionResponse)
def edit_transaction(txn_id: int, transaction:TransactionUpdate):

    updated = update_transaction(
        transaction.type,
        transaction.category,
        transaction.description,
        transaction.date,
        transaction.amount,
        transaction.project_id,
        txn_id
    )

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )

    return load_one_transaction(txn_id)
    

##PROJECTS##
class ProjectsCreate(BaseModel):
    name: str
    client_id: int | None = None
    start_date: date
    end_date: date
    estimated_revenue: float = Field(ge=0)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("End Date must be after the Start Date.")

        return self


class ProjectsResponse(BaseModel):
    id: int
    name: str
    client_id: int | None = None
    start_date: date
    end_date: date
    estimated_revenue: float 

class ProjectsUpdate(BaseModel):
    name: str
    client_id: int | None = None
    start_date: date
    end_date: date
    estimated_revenue: float = Field(ge=0)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("End Date must be after the Start Date.")

        return self

class ProjectFinanceReports(BaseModel):
    project_id: int
    transaction_count: int
    total_income: float
    total_expense: float
    profit: float



@app.get("/projects", response_model=list[ProjectsResponse])
def get_projects():
    return load_projects()


@app.get("/projects/{project_id}", response_model=ProjectsResponse)
def get_one_project(project_id: int):
    project = load_one_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project


@app.post("/projects")
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

@app.delete("/projects/{project_id}")   #HANDLE ACTIVE TRANSACTIONS, CANNOT DELETE
def del_project(project_id: int):
    deleted = delete_project(project_id)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Project Not Found."
        )

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }

@app.put("/projects/{project_id}", response_model=ProjectsResponse)
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


@app.get("/projects/{project_id}/summary", response_model=ProjectFinanceReports)
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