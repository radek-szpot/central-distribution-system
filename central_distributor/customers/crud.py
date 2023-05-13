from sqlalchemy.exc import SQLAlchemyError
from central_distributor.database import get_session
from central_distributor.customers.models import Customer
from sqlalchemy import select, insert


class CustomerCRUD:
    @staticmethod
    def create_customer(email, password, first_name, last_name, pan_number=None, cid_number=None, session=None):
        if not session:
            session = get_session()
        try:
            query = insert(Customer).values(email=email, password=password, first_name=first_name, last_name=last_name,
                                            pan_number=pan_number if pan_number else None,
                                            cid_number=cid_number if cid_number else None)
            customer = session.execute(query)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
        return customer

    @staticmethod
    def get_customer(customer_id):
        session = get_session()

        try:
            query = select(Customer).filter_by(id=customer_id)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer

    @staticmethod
    def get_customer_by_credentials(email, password):
        session = get_session()
        try:
            query = session.query(Customer).filter_by(email=email, password=password)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer

    @staticmethod
    def get_customer_list():
        session = get_session()
        try:
            customers = session.query(Customer).all()
        finally:
            session.close()
        return customers

    @staticmethod
    def delete_customer(customer_id):
        session = get_session()
        try:
            customer = session.query(Customer).filter_by(id=customer_id).first()
            if customer:
                session.delete(customer)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
