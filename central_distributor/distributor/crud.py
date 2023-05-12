from sqlalchemy.exc import SQLAlchemyError
from central_distributor.distributor.database import get_session, Product, Manufacturer


class ManufacturerCRUD:
    @staticmethod
    def create_manufacturer(url, session=None):
        if not session:
            session = get_session()

        try:
            manufacturer = Manufacturer(url=url)
            session.add(manufacturer)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
        return manufacturer

    @staticmethod
    def get_manufacturer(manufacturer_id, session=None):
        if not session:
            session = get_session()

        try:
            manufacturer = session.query(Manufacturer).filter_by(id=manufacturer_id).first()
        finally:
            session.close()
        return manufacturer

    @staticmethod
    def get_manufacturer_list(session=None):
        if not session:
            session = get_session()

        try:
            manufacturers = session.query(Manufacturer).all()
        finally:
            session.close()
        return manufacturers

    @staticmethod
    def delete_manufacturer(manufacturer_id, session=None):
        if not session:
            session = get_session()

        try:
            manufacturer = session.query(Manufacturer).filter_by(id=manufacturer_id).first()
            if manufacturer:
                session.delete(manufacturer)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


class ProductCRUD:
    @staticmethod
    def create_product(manufacturer_id, product_type, quantity, session=None):
        if not session:
            session = get_session()
        try:
            product = Product(manufacturer_id=manufacturer_id, type=product_type, quantity=quantity)
            session.add(product)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
        return product

    @staticmethod
    def get_product(product_id, session=None):
        if not session:
            session = get_session()

        try:
            product = session.query(Product).filter_by(id=product_id).first()
        finally:
            session.close()
        return product

    @staticmethod
    def get_product_list(session=None):
        if not session:
            session = get_session()

        try:
            products = session.query(Product).all()
        finally:
            session.close()
        return products

    @staticmethod
    def delete_product(product_id, session=None):
        if not session:
            session = get_session()

        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                session.delete(product)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


class CustomerCRUD:
    @staticmethod
    def create_customer(email, password, first_name, last_name, credit_card=None, session=None):
        if not session:
            session = get_session()
        if credit_card:
            pan_number = credit_card[0]
            cid_number = credit_card[1]
        try:
            customer = Customer(email=email, password=password, first_name=first_name, last_name=last_name,
                                credit_card=credit_card)
            session.add(customer)
            session.commit()
            return customer
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_customer(customer_id):
        session = get_session()

        try:
            customer = session.query(Customer).filter_by(id=customer_id).first()
            return customer
        finally:
            session.close()

    @staticmethod
    def get_customer_by_email(email):
        session = get_session()

        try:
            customer = session.query(Customer).filter_by(email=email).first()
            return customer
        finally:
            session.close()

    @staticmethod
    def get_customer_list():
        session = get_session()

        try:
            customers = session.query(Customer).all()
            return customers
        finally:
            session.close()

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
