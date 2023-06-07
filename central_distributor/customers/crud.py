from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from central_distributor.customers.models import Customer, Purchase
from central_distributor.customers.serializers import \
    purchase_history_serializer
from central_distributor.database import get_session
from central_distributor.distributor.models import Manufacturer, Product


class CustomerCRUD:
    @staticmethod
    def create(email, password, first_name, last_name, pan_number=None, cid_number=None, session=None):
        if not session:
            session = get_session()
        try:
            customer = Customer(email=email, password=password, first_name=first_name, last_name=last_name,
                                pan_number=pan_number, cid_number=cid_number)
            session.add(customer)
            session.commit()
            session.refresh(customer)
        except (SQLAlchemyError, IntegrityError):
            session.rollback()
            raise
        finally:
            session.close()
        return customer

    @staticmethod
    def get(customer_id, session=None):
        if not session:
            session = get_session()

        try:
            query = select(Customer).filter_by(id=customer_id)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer[0] if customer else None

    @staticmethod
    def get_by_credentials(email, password, session=None):
        if not session:
            session = get_session()
        try:
            query = session.query(Customer).filter_by(email=email, password=password)
            customer = session.execute(query).fetchone()
        finally:
            session.close()
        return customer[0] if customer else None

    @staticmethod
    def list(session=None):
        if not session:
            session = get_session()
        try:
            customers = session.query(Customer).all()
        finally:
            session.close()
        return customers

    @staticmethod
    def update(customer_id, session=None, **kwargs):
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
    def delete(customer_id, session=None):
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
    def create(customer_id: int, product_id: int, quantity: int, session=None):
        if not session:
            session = get_session()

        purchase = Purchase(customer_id=customer_id, product_id=product_id, quantity=quantity)
        session.add(purchase)
        session.commit()
        session.refresh(purchase)
        return purchase

    @staticmethod
    def get(purchase_id: int, session=None):
        if not session:
            session = get_session()

        return session.query(Purchase).filter(Purchase.id == purchase_id).first()

    @staticmethod
    def get_history(customer_id: int, session=None):
        if not session:
            session = get_session()

        purchase_product_query = (
            session.query(Purchase)
            .join(Product)
            .filter(Purchase.customer_id == customer_id)
            .with_entities(Purchase, Product.type, Product.singular_price, Manufacturer.name)
            .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
            .subquery()
        )
        purchases = session.query(*purchase_product_query.c).all()
        session.close()

        return [purchase_history_serializer(purchase) for purchase in purchases]

    @staticmethod
    def get_all_fields(customer_id: int, product_id: int, status: str, session=None):
        if not session:
            session = get_session()

        return session.query(Purchase).filter(
            Purchase.customer_id == customer_id,
            Purchase.product_id == product_id,
            Purchase.status == status,
        ).first()

    @staticmethod
    def list():
        session = get_session()
        try:
            purchase = session.query(Purchase).all()
        finally:
            session.close()
        return purchase

    @staticmethod
    def update(purchase_id: int, quantity: int = None, session=None):
        if not session:
            session = get_session()

        purchase = PurchaseCRUD.get(purchase_id, session)
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

        purchase = PurchaseCRUD.get(purchase_id, session)
        if purchase:
            session.delete(purchase)
            session.commit()
        return purchase
