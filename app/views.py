from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()

### Z ZAJĘĆ ###

"""
@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)
"""

### ZAD. 5.1 ###

@router.get("/suppliers", response_model=List[schemas.AllSuppliers])
async def get_all_suppliers(db: Session = Depends(get_db)):
    return crud.get_all_suppliers(db)

@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

### ZAD. 5.2 ###

@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.SupplierProduct])
async def get_supplier_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_products = crud.get_supplier_products(db, supplier_id)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_products

### ZAD. 5.3 ###

@router.post("/suppliers", response_model=schemas.Supplier, status_code=201)
async def create_supplier(new_supplier: schemas.NewSupplier, db: Session = Depends(get_db)):
    db_new_supplier = crud.create_new_supplier(db, new_supplier)
    return db_new_supplier

### ZAD. 5.4 ###

@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def update_supplier(supplier_id: PositiveInt, new_supplier: schemas.UpdateSupplier, db: Session = Depends(get_db)):
    db_updated_supplier = crud.update_supplier(db, supplier_id, new_supplier)
    if db_updated_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_updated_supplier