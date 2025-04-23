from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Customer, CustomerCategory

router = APIRouter(prefix="/customer", tags=["Customer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_customer(data: dict, db: Session = Depends(get_db)):
    if not data.get("name", "").strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty.")

    customer = Customer(name=data["name"])
    db.add(customer)
    db.commit()
    db.refresh(customer)

    for cat in data.get("categories", []):
        category = CustomerCategory(customer_id=customer.id, category_name=cat)
        db.add(category)
    db.commit()

    return JSONResponse(content={"customer_id": customer.id}, status_code=status.HTTP_201_CREATED)

@router.put("/{customer_id}")
def update_customer(customer_id: int, data: dict, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    customer.name = data["name"]
    db.query(CustomerCategory).filter(CustomerCategory.customer_id == customer_id).delete()

    # for cat in data.get("categories", []):
    #     category = CustomerCategory(customer_id=customer.id, category_name=cat)
    #     db.add(category)
    # db.commit()

    return {"message": "Customer updated."}

@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    categories = db.query(CustomerCategory).filter(CustomerCategory.customer_id == customer_id).all()
    return {
        "id": customer.id,
        "name": customer.name,
        "categories": [c.category_name for c in categories]
    }
