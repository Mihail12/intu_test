import datetime
import enum

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class ModelMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
    all_genders = "All_Genders"


class CategoryType(db.Model):
    __tablename__ = 'category_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class Retailer(db.Model, ModelMixin):
    __tablename__ = 'retailer'
    name = db.Column(db.String(64), unique=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.all_genders, nullable=False)
    type = db.relationship('CategoryType', backref='retailers', lazy=True)
    type_id = db.Column(db.Integer, db.ForeignKey('category_type.id'), nullable=False)


class Category(db.Model, ModelMixin):
    __tablename__ = 'category'
    name = db.Column(db.String(64), unique=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.all_genders, nullable=False)

    retailer = db.relationship('Retailer', backref='retailer', lazy=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)

    type = db.relationship('CategoryType', backref='categories', lazy=True)
    type_id = db.Column(db.Integer, db.ForeignKey('category_type.id'), nullable=False)

