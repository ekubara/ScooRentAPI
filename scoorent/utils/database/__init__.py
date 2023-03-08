from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from scoorent.data.settings import database_settings


engine = create_engine(
    f'mysql+pymysql://{database_settings.username}:{database_settings.password}'
    f'@localhost/{database_settings.database_name}'
)

Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=True)
database_session = Session()


def save_changes(entity=None):
    if entity:
        database_session.add(entity)
    database_session.commit()
    if entity:
        database_session.refresh(entity)
