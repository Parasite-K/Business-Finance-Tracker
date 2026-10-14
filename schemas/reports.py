from pydantic import BaseModel




class FinancialSummary(BaseModel):
    transaction_count: int
    total_income: float
    total_expense: float
    profit: float

class MonthlyReport(BaseModel):
    transaction_count: int
    total_income: float
    total_expense: float
    profit: float

class YearlyReport(BaseModel):
    transaction_count: int
    total_income: float
    total_expense: float
    profit: float

class CategoryReport(BaseModel):
    transaction_count: int
    category_total: float