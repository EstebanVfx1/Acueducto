from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://adsofull:Manolos2024!@45.63.105.150:3306/acueducto"
#DATABASE_URL = "mysql+pymysql://root:@localhost:3306/acueducto"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()