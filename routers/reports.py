from fastapi import APIRouter, Query, HTTPException
from typing import Literal
from schemas.reports import(
    YearlyReport,
    MonthlyReport,
    CategoryReport,
    FinancialSummary
)
from reports import(
    financial_summary,
    monthly_report,
    yearly_report,
    category_report
)
from data import categories
router = APIRouter()






@router.get("/reports/summary", response_model=FinancialSummary)
def get_financial_summary():
    txn_count, income, expense = financial_summary()

    return {
        "transaction_count": txn_count,
        "total_income": income,
        "total_expense": expense,
        "profit": income - expense
    }




@router.get("/reports/monthly", response_model=MonthlyReport)
def get_monthly_reports(
    year: int,
    month: int = Query(ge=1, le=12)
):
    txn_count, income, expense = monthly_report(year, month)

    return {
        "transaction_count": txn_count,
        "total_income": income,
        "total_expense": expense,
        "profit": income - expense
    }



@router.get("/reports/yearly", response_model=YearlyReport)
def get_yearly_reports(
    year: int,
):
    txn_count, income, expense = yearly_report(year)

    return {
        "transaction_count": txn_count,
        "total_income": income,
        "total_expense": expense,
        "profit": income - expense
    } 


@router.get("/reports/category", response_model=CategoryReport)
def get_category_reports(
    type: Literal["income", "expense"],
    category: str
):
    matched_category = None

    for valid_category in categories[type]:
        if valid_category.lower() == category.lower():
            matched_category = valid_category
            break

    if matched_category is None:
        raise HTTPException(
            status_code=400,
            detail="Category does not match the transaction type."
        )

    txn_count, total = category_report(type, matched_category)

    return {
        "transaction_count": txn_count,
        "category_total": total
    }