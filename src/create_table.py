from sqlalchemy import create_engine, Column, String, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def create_table(conn_url, table_name):
    engine = create_engine(conn_url, echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base = declarative_base()

    # Create table class that will inherit from Base class
    class Crypto(Base):
        __tablename__ = table_name

        symbol = Column(String(5), primary_key=True)
        symbol_name = Column(String(50))
        open = Column(Float)
        close = Column(Float)
        high = Column(Float)
        low = Column(Float)
        volume = Column(Float)
        date = Column(Date, primary_key=True)
        insert_date = Column(Date)

        def __init__(
            self, symbol, symbol_name, open, close, high, low, volume, date, insert_date
        ):
            self.symbol = symbol
            self.symbol_name = symbol_name
            self.open = open
            self.close = close
            self.high = high
            self.low = low
            self.volume = volume
            self.date = date
            self.insert_date = insert_date

    # creates table into database if not exists
    Base.metadata.create_all(engine, checkfirst=True)
