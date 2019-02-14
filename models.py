from sqlalchemy import create_engine, Table
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()

# association table
post_keywords = Table('ouvrage_components', Base.metadata,
    Column('ouvrage', ForeignKey('ouvrage.id'), primary_key=True),
    Column('component', ForeignKey('ouvrage.id'), primary_key=True),
    Column('component_formula', String, default=1),
    Column('position', Integer)
)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)


class Ouvrage(Base):
    __tablename__ = 'ouvrages'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    is_in_owner_library = Column(Boolean, default=False)
    name = Column(String)
    category = relationship(
        Category,
        backref=backref('ouvrages',
                        uselist=True,
                        cascade='delete,all'))
    created_on = Column(DateTime, default=func.now())
    unit = Column(String)
    height = Column(Float)
    width = Column(Float)
    stroke = Column(Float)
    up = Column(Float)

    components = relationship('Ouvrage',
            secondary=ouvrage_components,
            back_populates='ouvrages using it')
