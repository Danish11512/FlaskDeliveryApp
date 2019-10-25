# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB
)
from flask_login import (
    UserMixin,
    AnonymousUserMixin
)
from flaskdeliveryapp.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from app.constants import (
    permission,
    role_name,
)
from flaskdeliveryapp.extensions import bcrypt
import pytz
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

class Role(db.Model):
    """Roles for every user"""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.BigInteger)

    @classmethod
    def populate(cls):
            
        roles = {
            role_name.ANONYMOUS:(
                permission.ORDER |
                permission.PAY
            ),
            role_name.CUSTOMER:(
                permission.ORDER |
                permission.PAY |
                permission.COMMENT
            ),
            role_name.DELIVERYPERSON:(
                permission.BID |
                permission.ROUTES |
                permission.CUSTOMER_COMMENT
            ), 
            role_name.COOK: (
                permission.FOOD_QUALITY |
                permission.MENU |
                permission.PRICES 
            ),
            role_name.SALESPERSON: (
                permission.SUPPLIER
            )
            role_name.MANAGER:(
                permission.COMMISSIONS |
                permission.PAY |
                permission.COMPLAINTS |
                permission.MANAGEMENT
            ),
            role_name.ADMIN:(
                permission.ORDER |
                permission.PAY |
                permission.ORDER |
                permission.PAY |
                permission.COMMENT |
                permission.BID |
                permission.ROUTES |
                permission.CUSTOMER_COMMENT | 
                permission.FOOD_QUALITY |
                permission.MENU |
                permission.PRICES |
                permission.SUPPLIER | 
                permission.COMMISSIONS |
                permission.PAY |
                permission.COMPLAINTS |
                permission.MANAGEMENT
            )

        }

        for name, value in roles.items():
            role = Roles.query.filter_by(name=name).first()
            if role is None:
                role = cls(name=name)
            role.permissions = value
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Roles %r>' % self.id

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name})>".format(name=self.name)


class User(UserMixin, Model):
    """A user of the app."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    first_name = Column(db.String(30), nullable=True)
    middle_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    password = Column(db.LargeBinary(128), nullable=True)
    phone_number = Column(db.string(25), nullable=True)
    address = Column(db.string(200), nullable=True)
    active = Column(db.Boolean(), default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    stars = db.Column(db.Integer, default=0)
    salary = db.Column(db.Integer, default=0)
    commision = db.Column(db.Integer, default=10)
    credit_card = db.Column(db.Integer(10), nullable=True, default=None)
    csv = db.Column(db.Integer(3), nullable=True, default=None)


    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)
