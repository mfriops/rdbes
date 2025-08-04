#!/usr/local/bin/python3
# coding: utf-8

from __future__ import annotations

from sqlalchemy import Column, Float, Integer, Numeric, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

class Base(DeclarativeBase):
    """Declarative base class."""

# --- vessel --------------------------------------------------------------
class Vessel(Base):
    __tablename__ = "vessel_v"
    __table_args__ = {"schema": "vessel"}
    vessel_id = Column(Integer, primary_key=True)
    registration_no = Column(Integer)
    usage_category_no = Column(Integer)
    length = Column(Numeric)
    power_kw = Column(Numeric)
    brutto_weight_tons = Column(Numeric)
    home_port_no = Column(Integer, nullable=True)
