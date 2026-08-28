from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Invoice
from database import get_db
from auth import require_user

router = APIRouter()

class InvoiceCreate:
    title: str
    amount: float
    status: str  # 'paid' or 'unpaid'

class InvoiceUpdate:
    title: str | None = None
    amount: float | None = None
    status: str | None = None  # 'paid' or 'unpaid'

@router.post("/invoices/", response_model=Invoice)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    db_invoice = Invoice(title=invoice.title, amount=invoice.amount, status=invoice.status, user_id=user.id)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/invoices/", response_model=list[Invoice])
def read_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoices = db.query(Invoice).filter(Invoice.user_id == user.id).offset(skip).limit(limit).all()
    return invoices

@router.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/invoices/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: int, invoice: InvoiceUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.title is not None:
        db_invoice.title = invoice.title
    if invoice.amount is not None:
        db_invoice.amount = invoice.amount
    if invoice.status is not None:
        db_invoice.status = invoice.status

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.delete("/invoices/{invoice_id}", response_model=dict)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(db_invoice)
    db.commit()
    return {"detail": "Invoice deleted successfully"}
