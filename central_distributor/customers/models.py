from sqlalchemy import Column, Integer, String, Numeric
from central_distributor.database import Base


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    pan_number = Column(Numeric, nullable=True)
    cid_number = Column(Numeric, nullable=True)

    def __repr__(self):
        return f"<Customer(id={self.id}, email={self.email}, first_name={self.first_name} last_name={self.last_name})>"
