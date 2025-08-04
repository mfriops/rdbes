
from sqlalchemy import Column, Integer, Numeric, String, DateTime, between
from sqlalchemy.orm import DeclarativeBase

# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Declarative base class."""

# --- FishingTrip --------------------------------------------------------------
class Landings(Base):
    __tablename__ = "aflagrunnur"
    __table_args__ = {"schema": "agf"}
    londun_id = Column(Integer, primary_key=True)
    skip_numer = Column(Integer)
    londun_hefst = Column(DateTime)
    hafnarnumer = Column(Integer)
    vigtunartegund = Column(String(2))
    veidarfaeri = Column(Integer)
    veidistofn = Column(Integer)
    fisktegund = Column(Integer)
    astand = Column(Integer)
    geymsluadferd = Column(Integer)
    veidisvaedi = Column(String(2))
    afdrif = Column(String(1))
    fullvinnsla = Column(Integer)
    magn_oslaegt = Column(Numeric)
    magn_slaegt = Column(Numeric)
    magn = Column(Numeric)
    stada = Column(Integer)
    er_lokud = Column(Integer)
