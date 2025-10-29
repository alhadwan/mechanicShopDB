from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base) # Initialize SQLAlchemy with the Base class and connects Base to Flask-SQLAlchemy




# Association table for many-to-many relationship between mechanics and service tickets
mechanic_service = db.Table(
    'mechanic_service',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)


class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    # Relationship with service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(db.Date)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    # Relationships
    customer: Mapped['Customers'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanics']] = db.relationship(secondary=mechanic_service, back_populates='service_tickets')


class Mechanics(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    specialties: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # Relationship with service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=mechanic_service, back_populates='mechanics')