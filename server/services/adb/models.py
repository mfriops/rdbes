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
# Changed to fishing_trip_v because of duplicate records/fishing_trips
# see: select * from adb.fishing_trip where id like '163136%'
# Some have no fishing_station so this excludes them
class FishingTrip(Base):
    __tablename__ = "fishing_trip_v"
    __table_args__ = {"schema": "adb"}
    id = Column(String(255), primary_key=True)
    vessel_no = Column(Integer)
    departure = Column(DateTime)
    departure_port_no = Column(Integer)
    landing = Column(DateTime)
    landing_port_no = Column(Integer)

# --- FishingOperation --------------------------------------------------------------
class FishingStation(Base):
    __tablename__ = "fishing_station"
    __table_args__ = {"schema": "adb"}
    fishing_station_id = Column(Integer, primary_key=True)
    fishing_trip_id = Column(String(255))
    fishing_gear_no = Column(Integer)
    fishing_start = Column(DateTime)
    fishing_end = Column(DateTime)
    latitude = Column(Integer)
    longitude = Column(Integer)
    latitude_end = Column(Integer)
    longitude_end = Column(Integer)

# --- TargetAssemblage --------------------------------------------------------------
class TrawlAndSeineNet(Base):
    __tablename__ = "trawl_and_seine_net"
    __table_args__ = {"schema": "adb"}
    fishing_station_id = Column(Integer, primary_key=True)
    headline = Column(Integer)
    bridle = Column(Integer)
    mesh_size = Column(Integer)
    mesh_type = Column(String(3))
    grid_no = Column(String(50))
    square_window = Column(Integer)
    otterboard_weight = Column(Integer)
    circumference_mesh_number = Column(Integer)
    rope = Column(Integer)
    two_fg = Column(Integer)

class TargetAssemblage(Base):
    __tablename__ = "target_assemblage_v"
    __table_args__ = {"schema": "adb"}
    fishing_trip_id = Column(String(255), primary_key=True)
    registration_no = Column(Integer)
    species_no = Column(Integer)
    departure_date = Column(DateTime)
    landing_date = Column(DateTime)
    landing_year = Column(String(4))
    quantity = Column(Numeric)
    catch_type = Column(String(12))
    stations_cnt = Column(Integer)

class TargetStationAssemblage(Base):
    __tablename__ = "target_station_assemblage_v"
    __table_args__ = {"schema": "adb"}
    fishing_station_id = Column(Integer, primary_key=True)
    fishing_trip_id = Column(String(255))
    registration_no = Column(Integer)
    fishing_gear_no = Column(Integer)
    fishing_start = Column(DateTime)
    fishing_end = Column(DateTime)
    latitude = Column(Integer)
    longitude = Column(Integer)
    latitude_end = Column(Integer)
    longitude_end = Column(Integer)
    species_no = Column(Integer)
    quantity = Column(Numeric)
