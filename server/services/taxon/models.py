
from sqlalchemy import Column, Float, Integer, Numeric, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    """Declarative base class."""

# --- Species ----------------------------------------------------------------
class Species(Base):
    __tablename__ = "species"
    __table_args__ = {"schema": "taxon"}
    species_no = Column(Integer, primary_key=True)
    name = Column(String(60))
    eng_name = Column(String(60))
    sci_name = Column(String(60))
    # worms_id = Column(Integer)
    # code_3a = Column(String(3))
