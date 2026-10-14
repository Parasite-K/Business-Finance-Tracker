from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from data import categories

class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float = Field(ge=0)
    project_id: int | None = None

    @model_validator(mode="after")
    def validate_category(self):
        category = None
        for valid_category in categories[self.type]:
            if valid_category.lower() == self.category.lower():
                category = valid_category
                break
        if category is None:
            raise ValueError("Category does not match the transaction type.")

        self.category = category
        return self

class TransactionResponse(BaseModel):
    id: int
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float
    project_id: int | None

class PaginatedTransactionResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TransactionResponse]

class TransactionUpdate(BaseModel):
    type: Literal["income", "expense"]
    category: str
    description: str
    date: date
    amount: float = Field(ge=0)
    project_id: int | None = None

    @model_validator(mode="after")
    def validate_category(self):
        category = None
        for valid_category in categories[self.type]:
            if valid_category.lower() == self.category.lower():
                category = valid_category
                break
        if category is None:
            raise ValueError("Category does not match the transaction type.")

        self.category = category
        return self