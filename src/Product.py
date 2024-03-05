import logging
from db import db

log = logging.getLogger(__name__)
class Product(db.Model):
    __tablename__ = 'products'

    prod_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, prod_id, name):
        self.prod_id = prod_id
        self.name = name

    @classmethod
    def find_by_prod_id(cls, _prod_id):
        log.debug(f'find product by prod_id: {_prod_id}')
        return cls.query.get(_prod_id)
    
    @classmethod
    def find_all(cls):
        log.debug('Query for all products')
        return cls.query.all()
    
    def save_to_db(self):
        log.debug(f'Save product to database: prod_id={self.prod_id}, name={self.name}')
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        log.debug(f'Delete product from database: prod_id={self.prod_id}, name={self.name}')
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        return {
            "prod_id" : self.prod_id,
            "name" : self.name
        }
