#!/usr/local/bin/python3
# coding: utf-8

import os
import oracledb                      # Oracle Python driver
from typing import Any, Dict
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------

# ───────────────────────────── connection ──────────────────────────────
CONNECT_ARGS: Dict[str, Any] = {
    "user": os.getenv("DB_RDBES_USR"),
    "password": os.getenv("DB_RDBES_PWD"),
    "dsn": os.getenv("DB_RDBES_DSN"),
    "cclass": "RDBES_API",
    "purity": oracledb.ATTR_PURITY_SELF,
}

SCHEMA = (
    os.getenv("DB_RDBES_SCHEMA", CONNECT_ARGS["user"]).upper()
    if CONNECT_ARGS["user"]
    else None
)
# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""


# --- Harbour ------------------------------------------------------------
class Harbour(Base):
    __tablename__ = "harbour"
    __table_args__ = {"schema": SCHEMA.lower()}
    locode = Column(String(10), primary_key=True)
    name = Column(String(60))
    port_no = Column(Integer)


# --- Area ---------------------------------------------------------------
class Area(Base):
    __tablename__ = "area"
    __table_args__ = {"schema": SCHEMA.lower()}
    code = Column(String(12), primary_key=True)
    name = Column(String(60))


# --- Metier -------------------------------------------------------------
class Metier(Base):
    __tablename__ = "metier"
    __table_args__ = {"schema": SCHEMA.lower()}
    area_code = Column(String(12))
    metier = Column(String(20), primary_key=True)
    gear_type = Column(String(3))
    target_assemblage = Column(String(3))
    mesh_size_from = Column(Integer)
    mesh_size_to = Column(Integer)

