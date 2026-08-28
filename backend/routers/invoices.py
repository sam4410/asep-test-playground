from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Invoice
from database import get_db
from auth import require_user

router = APIRouter()

@router.post("/invoices/", response_model=Invoice)
def create_invoice(invoice: Invoice, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice.user_id = user.id  # Associate the invoice with the authenticated user
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/invoices/", response_model=List[Invoice])
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
def update_invoice(invoice_id: int, updated_invoice: Invoice, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.client_name = updated_invoice.client_name
    invoice.amount = updated_invoice.amount
    invoice.status = updated_invoice.status
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/invoices/{invoice_id}", response_model=Invoice)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(invoice)
    db.commit()
    return invoice
