class ExpenseRetrieve(BaseModel):
    id: int
    amount: float
    category: str
    date: str
    user_id: int

@router.get("/expenses", response_model=list[ExpenseRetrieve])
def get_expenses_by_category(category: str, db: Session = next(get_db())):
    expenses = db.query(Expense).filter(Expense.category == category).all()
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this category")
    return expenses
    
app.include_router(router)