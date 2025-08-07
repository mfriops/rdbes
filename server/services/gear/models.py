#!/usr/local/bin/python3
# coding: utf-8

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    """Declarative base class."""


# --- gear ----------------------------------------------------------------
class FishingGear(Base):
    __tablename__ = "fishing_gear"
    __table_args__ = {"schema": "gear"}
    fishing_gear_no = Column(Integer, primary_key=True)
    isscfg_no = Column(String(4))


class Isscfg(Base):
    __tablename__ = "isscfg"
    __table_args__ = {"schema": "gear"}
    isscfg_no = Column(String(4), primary_key=True)
    gear_category = Column(String(40))
    stand_no = Column(String(4))
