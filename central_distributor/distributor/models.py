from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from central_distributor.database import Base


class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    products = relationship('Product', back_populates='manufacturer')

    def __repr__(self):
        return f"<Manufacturer(id={self.id}, url={self.url})>"


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    singular_price = Column(Float, nullable=False)
    manufacturer = relationship('Manufacturer', back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, type={self.type}, quantity={self.quantity}, price={self.singular_price})>"
