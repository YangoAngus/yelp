from sqlalchemy import (
    create_engine,
    Column,
    func,
    ForeignKey
    )
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from scrapy.utils.project import get_project_settings
from sqlalchemy import Table
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
)


Base = declarative_base()
engine = create_engine(get_project_settings().get(
        'CONNECTION_STRING',
        ),
    convert_unicode=True,
    pool_size=10000,
    max_overflow=10200,
)

def init_db():
    Base.metadata.create_all(engine)


business_location_association = Table('business_location_association',
                                           Base.metadata,
                                           Column('business_id',
                                                  INTEGER,
                                                  ForeignKey('business.id'),
                                                  nullable=False),
                                           Column('location_id',
                                                  INTEGER,
                                                  ForeignKey('location.id'),
                                                  nullable=False)
                                      )
business_category_association = Table('business_category_association',
                                      Base.metadata,
                                      Column('business_id',
                                             INTEGER,
                                             ForeignKey('business.id'),
                                             nullable=False),
                                      Column('category_id',
                                             ForeignKey('category.id'),
                                             nullable=False),
                                      )

class Category(Base):
    __tablename__ = 'category'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), unique=True,
                  nullable=False)
    business = relationship(
        'Business',
        secondary=business_category_association,
        back_populates='category')
    def __repr__(self):
        return '{}'.format(self.name)
    
class Location(Base):
    __tablename__ = 'location'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), unique=True,
                  nullable=False)
    business = relationship(
        'Business',
        secondary=business_location_association,
        back_populates='location')
    def __repr__(self):
        return '{}'.format(self.name)
    
class Business(Base):
    __tablename__ = 'business'
    id = Column(INTEGER, primary_key=True)
    title = Column(VARCHAR(1000), nullable=False)
    source_url = Column(VARCHAR(1000), unique=True,
                        nullable=False)
    address = Column(JSON, nullable=False)
    telephone = Column(VARCHAR(20), nullable=False)
    website = Column(VARCHAR(100), nullable=False)
    timetable = Column(JSON, nullable=False)
    about = Column(LONGTEXT, nullable=False)
    images = Column(JSON, nullable=False)
    reviews = Column(INTEGER, nullable=False)
    add_time = Column(DATETIME, default=func.now(),
                      nullable=False)
    update_version = Column(INTEGER, default=0,
                            nullable=False)
    update_time = Column(DATETIME, default=func.now(),
                         nullable=False)
    location = relationship(
        'Location', secondary=business_location_association,
        back_populates='business'
    )
    category = relationship(
        'Category',
        secondary=business_category_association,
        back_populates='business')
    def __repr__(self):
        return '{}'.format(self.title)