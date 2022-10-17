import os
import json
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import date


def remove(root_dir):

    file_path = os.path.join(root_dir, "tmp", "cryptos.json")
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("File has been deleted")
    else:
        print("File does not exist")


def populate(table_name: str, root_dir: str, conn_url: str):
    engine = create_engine(conn_url, echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    meta = MetaData()
    meta.reflect(bind=engine)

    mytable = meta.tables[table_name]

    full_dir = os.path.join(root_dir, "tmp", "cryptos.json")

    with open(full_dir, "r") as f:
        crypto_data = json.load(f)

    data_values = [
        {
            "open": float(i["1b. open (USD)"]),
            "close": float(i["4b. close (USD)"]),
            "high": float(i["2b. high (USD)"]),
            "low": float(i["3b. low (USD)"]),
            "volume": float(i["5. volume"]),
            "date": i["date"],
            "symbol": str(i["crypto_code"]),
            "symbol_name": str(i["crypto_name"]),
            "insert_date": date.today().strftime("%Y/%m/%d"),
        }
        for i in crypto_data
    ]

    conn = engine.connect()
    try:
        conn.execute(mytable.insert().values(data_values))
    except IntegrityError:
        session.rollback()
        print("Record already exists!")
    conn.close()
