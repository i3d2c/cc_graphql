from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, 
                            relation)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class OuvrageComponent(Base):
    __tablename__ = 'ouvrage_component'
    id = Column(Integer, primary_key=True)
    ouvrage_id = Column(Integer, ForeignKey('ouvrage.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('ouvrage.id'), nullable=False)
    ouvrage = relationship("Ouvrage", foreign_keys=[ouvrage_id])
    component = relationship("Ouvrage", foreign_keys=[component_id])

    component_formula = Column(String, default=1)
    position = Column(Integer)


class Ouvrage(Base):
    __tablename__ = 'ouvrage'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)
    is_in_owner_library = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', foreign_keys=[category_id])
    created_on = Column(DateTime, default=func.now())
    unit = Column(String)
    height = Column(Float)
    width = Column(Float)
    stroke = Column(Float)
    up = Column(Float)

    components = relationship("OuvrageComponent", back_populates="ouvrage", foreign_keys="[OuvrageComponent.component_id]")

    __table_args__ = (UniqueConstraint('name', 'owner_id', name='_name_owner_id'),)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)

    ouvrages = relationship('Ouvrage', back_populates='category')
    __table_args__ = (UniqueConstraint('name', 'owner_id', name='_name_owner_id'),)
