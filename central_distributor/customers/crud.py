from sqlalchemy.exc import SQLAlchemyError
from central_distributor.database import get_session
from central_distributor.customers.models import Customer, Purchase
from sqlalchemy import select, insert, update


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
    def get_customer(customer_id, session=None):
        if not session:
            session = get_session()

        try:
            query = select(Customer).filter_by(id=customer_id)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer[0] if customer else None

    @staticmethod
    def get_customer_by_credentials(email, password, session=None):
        if not session:
            session = get_session()
        try:
            query = session.query(Customer).filter_by(email=email, password=password)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer[0] if customer else None

    @staticmethod
    def get_customer_list(session=None):
        if not session:
            session = get_session()
        try:
            customers = session.query(Customer).all()
        finally:
            session.close()
        return customers

    @staticmethod
    def update_customer(customer_id, session=None, **kwargs):
        if not session:
            session = get_session()
        try:
            query = update(Customer).where(Customer.id == customer_id).values(**kwargs)
            session.execute(query)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete_customer(customer_id, session=None):
        if not session:
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


class PurchaseCRUD:
    @staticmethod
    def create_purchase(customer_id: int, product_id: int, quantity: int, session=None):
        if not session:
            session = get_session()

        purchase = Purchase(customer_id=customer_id, product_id=product_id, quantity=quantity)
        session.add(purchase)
        session.commit()
        session.refresh(purchase)
        return purchase

    @staticmethod
    def get_purchase(purchase_id: int, session=None):
        if not session:
            session = get_session()

        return session.query(Purchase).filter(Purchase.id == purchase_id).first()

    @staticmethod
    def get_purchase_all_filters(customer_id: int, product_id: int, session=None):
        if not session:
            session = get_session()

        return session.query(Purchase).filter(
            Purchase.customer_id == customer_id,
            Purchase.product_id == product_id
        ).first()

    @staticmethod
    def get_purchases():
        session = get_session()
        try:
            purchase = session.query(Purchase).all()
        finally:
            session.close()
        return purchase

    @staticmethod
    def update_purchase(purchase_id: int, quantity: int = None, session=None):
        if not session:
            session = get_session()

        purchase = PurchaseCRUD.get_purchase(purchase_id, session)
        if purchase:
            if quantity is not None:
                purchase.quantity += quantity
            session.commit()
            session.refresh(purchase)
        return purchase

    @staticmethod
    def delete_purchase(purchase_id: int, session=None):
        if not session:
            session = get_session()

        purchase = PurchaseCRUD.get_purchase(purchase_id, session)
        if purchase:
            session.delete(purchase)
            session.commit()
        return purchase
