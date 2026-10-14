from fastapi import APIRouter, HTTPException, Query
from psycopg.errors import ForeignKeyViolation
from typing import Literal
from data import categories

from datetime import date
from decimal import Decimal

from storage import (
    load_transactions, 
    save_transaction,
    load_one_transaction,
    delete_transaction,
    update_transaction,
)
from schemas.transactions import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    PaginatedTransactionResponse,
)

router = APIRouter()

@router.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    try:
        txn_id = save_transaction(
            transaction.type,
            transaction.category,
            transaction.description,
            transaction.date,
            transaction.amount,
            transaction.project_id    
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=400,
            detail="Specified Project Does Not Exist."
        )

    return {
        "message": "Transaction created successfully",
        "transaction_id": txn_id
    }



@router.get("/transactions", response_model=PaginatedTransactionResponse)
def get_transactions(
    type: Literal["income", "expense"] | None = None,
    category: str | None = None,
    project_id: int | None = None,
    min_amount: Decimal | None = Query(default=None, ge=0),
    max_amount: Decimal  | None = Query(default=None, ge=0),
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=422,
            detail="Minimum amount cannot be greater than Maximum amount."
        )

    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="End date cannot be before Start date."
        )
    matched_category = None
    if category is not None:
        if type is not None:
            for valid_category in categories[type]:
                if valid_category.lower() == category.lower():
                    matched_category = valid_category
                    break

            if matched_category is None:
                raise HTTPException(
                    status_code=422,
                    detail="Entered category does not exist or does not match transaction type."
                )
        else:
            matched_category = None
            for txn_type in categories:
                for check_category in categories[txn_type]:
                    if check_category.lower() == category.lower():
                        matched_category = check_category
                        break

                if matched_category is not None:
                    break

            if matched_category is None:
                raise HTTPException(
                    status_code=422,
                    detail="Entered category is invalid."
                )
                
        
    txns, txn_count = load_transactions(
                        txn_type=type,
                        category=matched_category,
                        project_id=project_id,
                        min_amount=min_amount,
                        max_amount=max_amount,
                        start_date=start_date,
                        end_date=end_date,
                        limit=limit,
                        offset=offset
                        ) 

    return {
        "total": txn_count,
        "limit": limit,
        "offset": offset,
        "items": txns
    }
    


@router.get("/transactions/{txn_id}", response_model=TransactionResponse)
def get_one_transaction(txn_id: int):
    transaction =  load_one_transaction(txn_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.delete("/transactions/{txn_id}")
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



@router.put("/transactions/{txn_id}", response_model=TransactionResponse)
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