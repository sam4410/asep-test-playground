from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Invoice
from database import get_db
from auth import require_user

router = APIRouter()

@router.get("/invoices")
def read_invoices(db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoices = db.query(Invoice).filter(Invoice.user_id == user.id).all()
    return invoices

@router.post("/invoices")
def create_invoice(invoice: Invoice, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice.user_id = user.id
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: int, updated_invoice: Invoice, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.client_name = updated_invoice.client_name
    invoice.amount = updated_invoice.amount
    invoice.status = updated_invoice.status
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return {"detail": "Invoice deleted successfully"}