from datetime import date

from pydantic import BaseModel, Field, model_validator



class ProjectsResponse(BaseModel):
    id: int
    name: str
    client_id: int | None = None
    start_date: date
    end_date: date
    estimated_revenue: float 

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
