from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from central_distributor.database import Base


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    pan_number = Column(Numeric, nullable=True)
    cid_number = Column(Numeric, nullable=True)

    purchases = relationship('Purchase', back_populates='customer')

    def __repr__(self):
        return f"<Customer(id={self.id}, email={self.email}, first_name={self.first_name} last_name={self.last_name})>"


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="Paid")

    customer = relationship('Customer', back_populates='purchases')
    product = relationship('Product', back_populates='purchases')

    def __repr__(self):
        return f"<Purchase(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, quantity={self.quantity})>"
