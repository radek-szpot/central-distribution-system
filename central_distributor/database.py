from sqlalchemy import create_engine, Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
# # Define the intermediary table for the many-to-many relationship
# customer_product_association = Table(
#     'customer_product_association',
#     Base.metadata,
#     Column('customer_id', Integer, ForeignKey('customer.id')),
#     Column('product_id', Integer, ForeignKey('product.id')),
#     Column('quantity', Integer, nullable=False)  # Add quantity column
# )


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
