#!/usr/local/bin/python3
# coding: utf-8

from sqlalchemy import Column, Integer, Numeric, String, DateTime, between
from sqlalchemy.orm import DeclarativeBase

# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Declarative base class."""

# --- FishingTrip --------------------------------------------------------------
class Quota(Base):
    __tablename__ = "afla_heimild"
    __table_args__ = {"schema": "kvoti"}
    id = Column(Integer, primary_key=True)
    skip_nr = Column(Integer)
    ftegund = Column(Integer)
    heimild = Column(String(1))
    magn = Column(Numeric)
    i_gildi = Column(DateTime)
    ur_gildi = Column(DateTime)
