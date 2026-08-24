from datetime import datetime

@router.get("/transactions/filter")
def get_filtered_transactions(
    category: str = None,
    start_date: str = None,
    end_date: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if category:
        query = query.filter(Transaction.category == category)

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.offset(skip).limit(limit).all()
    return transactions