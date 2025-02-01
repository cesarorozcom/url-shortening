from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table, 
    Column, 
    Integer, 
    String,
    ForeignKey
    )
from datetime import datetime

engine = create_engine('sqlite:///shorten_url.db', echo=True)

metadata = MetaData()

shorten_url_table = Table(
    'shorten_urls',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String, nullable=False),
    Column('short_code', String, nullable=False),
    Column('updated_at', String, nullable=True),
    Column('created_at', String, default=datetime.now())
)

shorten_url_table_stats = Table(
    'shorten_url_stats',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('shorten_url_id', ForeignKey('shorten_urls.id'), nullable=False),
    Column('access_count', Integer, default=0)
)

metadata.create_all(engine)