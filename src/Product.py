from db import db


class Product(db.Model):
    __tablename__ = 'products'

    prod_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, prod_id, name):
        self.prod_id = prod_id
        self.name = name

    @classmethod
    def find_by_prod_id(cls, _prod_id):
        return cls.query.get(_prod_id)
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        return {
            "prod_id" : self.prod_id,
            "name" : self.name
        }
