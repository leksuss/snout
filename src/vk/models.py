import enum

from sqlalchemy import Integer, String, BigInteger, ForeignKey, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date

from src.db_conn import Base


class SexEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class PublTypeEnum(enum.Enum):
    CLIP = 'clip'
    VIDEO = 'video'


class ActivityTypeEnum(enum.Enum):
    LIKE = 'like'
    COMMENT = 'comment'


class Publication(Base):
    __tablename__ = 'publications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    vk_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    type: Mapped[PublTypeEnum] = mapped_column(Enum(PublTypeEnum), nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship('User', back_populates='publications')
    activities = relationship('Activity', back_populates='publication')

    def __repr__(self):
        return f'Publication {self.type}{self.user.vk_id}_{self.vk_id}'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    vk_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[String] = mapped_column(String(255), nullable=True)
    last_name: Mapped[String] = mapped_column(String(255), nullable=True)
    nickname: Mapped[str] = mapped_column(String, nullable=True)
    sex: Mapped[SexEnum] = mapped_column(Enum(SexEnum), nullable=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    publications = relationship('Publication', back_populates='user')
    activities = relationship('Activity', back_populates='user')
    country = relationship('Country', back_populates='users')
    city = relationship('City', back_populates='users')

    def __repr__(self):
        return f'User ID {self.vk_id}'


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    vk_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users = relationship('User', back_populates='country')
    cities = relationship('City', back_populates='country')

    def __repr__(self):
        return f'Country {self.name} (ID {self.id}, VK_ID {self.vk_id})'


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    vk_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'))

    users = relationship('User', back_populates='city')
    country = relationship('Country', back_populates='cities')

    def __repr__(self):
        return f'City {self.name} (ID {self.id}, VK_ID {self.vk_id})'


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    publication_id: Mapped[int] = mapped_column(Integer, ForeignKey('publications.id'), nullable=False)
    type: Mapped[ActivityTypeEnum] = mapped_column(Enum(ActivityTypeEnum), nullable=False)

    user = relationship('User', back_populates='activities')
    publication = relationship('Publication', back_populates='activities')

    def __repr__(self):
        return f'{self.user} did {self.type} for publ {self.publication}'