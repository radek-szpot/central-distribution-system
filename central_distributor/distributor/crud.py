from sqlalchemy.exc import SQLAlchemyError
from central_distributor.database import get_session
from central_distributor.distributor.models import Product, Manufacturer
from sqlalchemy import select


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
    def create_product(manufacturer_id, product_type, quantity, price, session=None):
        if not session:
            session = get_session()
        try:
            product = Product(manufacturer_id=manufacturer_id, type=product_type, quantity=quantity,
                              singular_price=price)
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
