from datetime import datetime

from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, Boolean, NVARCHAR, text

from . import Base


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    phone_number = Column(NVARCHAR(15))
    first_name = Column(NVARCHAR(50))
    last_name = Column(NVARCHAR(50))
    email = Column(NVARCHAR(100))
    registration_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(
            self,
            phone_number: str,
            first_name: str,
            last_name: str,
            email: str
    ):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class Admins(Base):
    __tablename__ = "Admins"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(NVARCHAR(30))
    password = Column(NVARCHAR(150))
    can_get = Column(Boolean, default=True)
    can_create = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=True)
    can_delete = Column(Boolean, default=True)
    registration_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(
            self,
            username: str,
            password: str
    ):
        self.username = username
        self.password = password


class Scooters(Base):
    __tablename__ = "Scooters"

    id = Column(Integer, autoincrement=True, primary_key=True)
    scooter_name = Column(NVARCHAR(100))
    is_available = Column(Boolean, default=True)
    is_booked = Column(Boolean, default=False)
    booked_by_user_id = Column(Integer)
    booked_at_date = Column(TIMESTAMP)

    def __init__(self, scooter_name: str):
        self.scooter_name = scooter_name


class Cards(Base):
    __tablename__ = "Cards"

    id = Column(Integer, autoincrement=True, primary_key=True)
    owner_id = Column(Integer)
    card_image_path = Column(NVARCHAR(300))
    card_bank_name = Column(NVARCHAR(35))
    hashed_card_data = Column(NVARCHAR(150))
    four_last_digits = Column(Integer)

    def __init__(
            self,
            owner_id: int,
            card_image_path: str,
            card_bank_name: str,
            hashed_card_data: str,
            four_last_digits: int
    ):
        self.owner_id = owner_id
        self.card_image_path = card_image_path
        self.card_bank_name = card_bank_name
        self.hashed_card_data = hashed_card_data
        self.four_last_digits = four_last_digits


class Orders(Base):
    __tablename__ = "Orders"

    id = Column(Integer, autoincrement=True, primary_key=True)
    customer_id = Column(Integer)
    price = Column(DECIMAL(12, 2))
    is_active = Column(Boolean, default=False)
    booking_started_at = Column(TIMESTAMP)
    booking_finished_at = Column(TIMESTAMP)

    def __init__(
            self,
            customer_id: int,
            price: float,
            is_active: bool,
            booking_started_at: datetime,
            booking_finished_at: datetime
    ):
        self.customer_id = customer_id
        self.price = price
        self.is_active = is_active
        self.booking_started_at = booking_started_at
        self.booking_finished_at = booking_finished_at
