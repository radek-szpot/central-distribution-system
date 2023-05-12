from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    products = relationship('Product', back_populates='manufacturer')

    def __repr__(self):
        return f"<Manufacturer(id={self.id}, url={self.url})>"


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    type = Column(String)
    quantity = Column(Integer)
    singular_price = Column(Float)
    manufacturer = relationship('Manufacturer', back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, type={self.type}, quantity={self.quantity}, price={self.singular_price})>"


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    password = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    pan_number = Column(String)
    cid_number = Column(String)

    def __repr__(self):
        return f"<Customer(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"


def create_database():
    """Create the SQLite engine and tables"""
    engine = create_engine('sqlite:///inventory.db')
    Base.metadata.create_all(engine)


def get_session():
    """Create a session to interact with the database and return it"""
    engine = create_engine('sqlite:///inventory.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


create_database()
