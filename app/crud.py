from sqlalchemy.orm import Session

from . import models
from .schemas import NewSupplier, UpdateSupplier

from sqlalchemy import update

### Z ZAJĘĆ ###

"""
def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )
"""

### ZAD. 5.1 ###

def get_all_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()

def get_supplier(db: Session, supplier_id: int):
    return(db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first())

### ZAD. 5.2 ###

def get_supplier_products(db: Session, supplier_id:int):
    return db.query(models.Product).join(models.Category).filter(models.Product.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()).all()
    #return db.query(models.Product).join(models.Category).all()
    
### ZAD. 5.3 ###

def create_new_supplier(db: Session, new_supplier: NewSupplier):
    new_supplier_id = db.query(models.Supplier).count()+1
    new_supplier_output = models.Supplier(SupplierID = new_supplier_id,
                                          CompanyName = new_supplier.CompanyName,
                                          ContactName = new_supplier.ContactName,
                                          ContactTitle = new_supplier.ContactTitle,
                                          Address = new_supplier.Address,
                                          City = new_supplier.City,
                                          PostalCode = new_supplier.PostalCode,
                                          Country = new_supplier.Country,
                                          Phone = new_supplier.Phone)
    db.add(new_supplier_output)
    db.commit()
    return new_supplier_output

### ZAD. 5.4 ###

def update_supplier(db: Session, supplier_id: int, new_supplier: UpdateSupplier):
    supplier_dict=new_supplier.dict()
    if bool(supplier_dict):
        db.execute(update(models.Supplier).where(models.Supplier.SupplierID == supplier_id).values(**supplier_dict))
        db. commit()
    
    return get_supplier(db, supplier_id)
    