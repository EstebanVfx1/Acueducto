from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "mysql+pymysql:/manolos740:Manolos22!@207.246.65.47/acueducto"
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/acueducto"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
