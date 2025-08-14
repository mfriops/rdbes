#!/usr/local/bin/python3
# coding: utf-8

from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.orm import DeclarativeBase

# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    """Declarative base class."""

# --- Cruise --------------------------------------------------------------
class Cruise(Base):
    __tablename__ = "cruise"
    __table_args__ = {"schema": "channel"}
    cruise_id = Column(Integer, primary_key=True)
    cruise = Column(String(10), unique=True)
    departure = Column(DateTime)  # ideally DateTime
    arrival = Column(DateTime)

# --- Station --------------------------------------------------------------
class Station(Base):
    __tablename__ = "station"
    __table_args__ = {"schema": "channel"}
    station_id = Column(Integer, primary_key=True)
    cruise_id = Column(Integer)
    station_no = Column(Integer)
    station_date = Column(DateTime)
    latitude = Column(Integer)
    longitude = Column(Integer)
    latitude_end = Column(Integer)
    longitude_end = Column(Integer)
    globe_position = Column(Integer)
    vessel_no = Column(Integer)
    port_no = Column(Integer)

# --- Sample --------------------------------------------------------------
class Sample(Base):
    __tablename__ = "sample"
    __table_args__ = {"schema": "channel"}
    sample_id = Column(Integer, primary_key=True)
    station_id = Column(Integer)
    sample_category_no = Column(Integer)
    land_sample = Column(Integer)
    tow_start = Column(DateTime)
    tow_end = Column(DateTime)
    time_measure = Column(Integer)
    mesh_size = Column(Numeric)
    isscfg_no = Column(String(4))

# --- Measure --------------------------------------------------------------
class Measure(Base):
    __tablename__ = "measure"
    __table_args__ = {"schema": "biota"}
    measure_id = Column(Integer, primary_key=True)
    sample_id = Column(Integer)
    measure_type = Column(String(4))
    length = Column(Numeric, nullable=True)
    weight = Column(Numeric, nullable=True)
    sex_no = Column(Integer, nullable=True)
    species_no = Column(Integer, nullable=True)
    sexual_maturity_id = Column(Integer, nullable=True)

# --- Otolith --------------------------------------------------------------
class Otolith(Base):
    __tablename__ = "otolith"
    __table_args__ = {"schema": "biota"}
    measure_id = Column(Integer, primary_key=True)
    sample_id = Column(Integer)
    age = Column(Integer)
    otolith_type = Column(String(4))

# --- Speciee --------------------------------------------------------------
class Species(Base):
    __tablename__ = "species"
    __table_args__ = {"schema": "biota"}
    species_no = Column(Integer, primary_key=True)
    worms_id = Column(Integer)
    code_3a = Column(String(3))
    name = Column(String(60))
    eng_name = Column(String(60))

# --- SexualMaturity --------------------------------------------------------------
class SexualMaturity(Base):
    __tablename__ = "sexual_maturity"
    __table_args__ = {"schema": "biota"}
    sexual_maturity_id = Column(Integer, primary_key=True)
    sexual_maturity_no = Column(Integer)
