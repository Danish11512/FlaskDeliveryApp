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
from flaskdeliveryapp.constants import (
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
            ),
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
    db.metadata.clear()
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False) 
    email = Column(db.String(80), unique=True, nullable=False) 
    first_name = Column(db.String(30), nullable=True) 
    middle_initial = Column(db.String(2), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    password = Column(db.LargeBinary(128), nullable=True)
    phone_number = Column(db.String(25), nullable=True)
    address = Column(db.String(200), nullable=True)
    active = Column(db.Boolean(), default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    stars = db.Column(db.Integer, default=0)
    salary = db.Column(db.Integer, default=0)
    commision = db.Column(db.Integer, default=10)
    credit_card = db.Column(db.Integer, nullable=True, default=None)
    csv = db.Column(db.Integer, nullable=True, default=None)


    def __init__(self,
                 username,
                 first_name,
                 middle_initial,
                 last_name,
                 email,
                 phone_number,
                 role_id,
                 password, 
                 address, 
                 active, 
                 stars,
                 salary,
                 commision, 
                 credit_card,
                 csv):
        self.username = username
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.role_id = role_id
        self.set_password(password, update_history=False)  # only update on password resets
        self.address = address
        self.active = active
        self.stars = stars
        self.salary = salary
        self.commision = commision
        self.credit_card = credit_card
        self.csv = csv


    @property
    def name(self):
        """
        Property to return a User's full name, including middle initial if applicable.
        :return:
        """
        if self.middle_initial:
            return self.first_name + " " + self.middle_initial + " " + self.last_name
        return self.first_name + " " + self.last_name


    @property
    def has_invalid_password(self):

        """
        Returns whether the user's password is expired or is the default password (True) or not (False).
        """
        if current_app.config['USE_LOCAL_AUTH']:
            return datetime.utcnow() > self.expiration_date or self.check_password(current_app.config['DEFAULT_PASSWORD'])
        return False


    def is_new_password(self, password):
        """
        Returns whether the supplied password is not the same as the current
        or previous passwords (True) or not (False).
        """
        existing_passwords = list(filter(None, [self.password] + [h.password for h in self.history.all()]))
        return not existing_passwords or all(not check_password_hash(p, password) for p in existing_passwords)


    def set_password(self, password, update_history=True):
        if self.is_new_password(password):
            if update_history:
                # update previous passwords
                if self.history.count() >= self.MAX_PREV_PASS:
                    # remove oldest password
                    self.history.filter_by(  # can't call delete() when using order_by()
                        id=self.history.order_by(History.timestamp.asc()).first().id
                    ).delete()
                db.session.add(History(self.id, self.password))

            self.expiration_date = datetime.utcnow() + timedelta(days=self.DAYS_UNTIL_EXPIRATION)
            self.password = generate_password_hash(password)

            db.session.commit()


    def update_password(self, current_password, new_password):
        if self.check_password(current_password):
            self.set_password(new_password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    @classmethod
    def populate(cls):
        roles_dict = {}
        roles = Roles.query.all()
        for role in roles:
            roles_dict[role.name] = role.id

        with open(current_app.config['USER_DATA'], 'r') as data:
            dictreader = csv.DictReader(data)

            for row in dictreader:
                user = cls(
                    first_name=row['first_name'],
                    middle_initial=row['middle_initial'],
                    last_name=row['last_name'],
                    email=row['email'],
                    username=row['username'],
                    # phone_number=row['phone_number'], HERe
                    role_id=roles_dict[row['role']],
                    password=current_app.config['DEFAULT_PASSWORD']
                )
                db.session.add(user)
        db.session.commit()

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)



