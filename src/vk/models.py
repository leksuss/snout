import enum

from sqlalchemy import Integer, String, BigInteger, ForeignKey, Enum, Boolean, Table, Column, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date
from typing import List

from src.db_conn import Base


class SexEnum(enum.Enum):
    MALE = ' MALE'
    FEMALE = 'FEMALE'
    UNKNOWN = 'UNKNOWN'


class PublTypeEnum(enum.Enum):
    CLIP = 'CLIP'
    VIDEO = 'VIDEO'
    WALL = 'WALL'


class ActivityTypeEnum(enum.Enum):
    LIKE = 'LIKE'
    COMMENT = 'COMMENT'


class SnapshotStatusEnum(enum.Enum):
    SUCCESS = 'SUCCESS'
    NOT_FOUND = 'NOT_FOUND'
    ACCESS_DENIED = 'ACCESS_DENIED'
    ERROR = 'ERROR'


publication_hashtag = Table(
    'publications_hashtags',
    Base.metadata,
    Column('publication_id', Integer, ForeignKey('publications.id')),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'))
)


class Publication(Base):
    __tablename__ = 'publications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    id_vk: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    date_published: Mapped[Date] = mapped_column(Date, nullable=False)
    type: Mapped[PublTypeEnum] = mapped_column(Enum(PublTypeEnum), nullable=False)

    user = relationship('User', back_populates='publications')

    hashtags: Mapped[List['Hashtag']] = relationship(
        'Hashtag',
        secondary=publication_hashtag,
        back_populates='publications'
    )
    activities = relationship('Activity', back_populates='publication')
    snapshots = relationship('PublicationSnapshot', back_populates='publication')

    __table_args__ = (
        UniqueConstraint('id_vk', 'user_id', name='unique_publ'),
    )

    def __repr__(self):
        return f'https://vk.com/{self.type.value.lower()}{self.user.id_vk}_{self.id_vk}'


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey('campaigns.id'))
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=True)

    publications: Mapped[List['Publication']] = relationship(
        'Publication',
        secondary=publication_hashtag,
        back_populates='hashtags'
    )

    campaign = relationship('Campaign', cascade='all, delete', back_populates='hashtags')

    __table_args__ = (
        UniqueConstraint('name', 'campaign_id', name='unique_hashtag_in_campaign'),
    )

    def __repr__(self):
        return f'Hashtag {self.name}'


class Campaign(Base):
    __tablename__ = 'campaigns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    hashtags = relationship('Hashtag', cascade='all, delete', back_populates='campaign')

    def __repr__(self):
        return f'Campaign {self.name}'


class PublicationSnapshot(Base):
    __tablename__ = 'publication_snapshots'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, autoincrement=True, index=True)
    publication_id: Mapped[int] = mapped_column(Integer, ForeignKey('publications.id'), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comments: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    checked_at: Mapped[Date] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    status: Mapped[SnapshotStatusEnum] = mapped_column(Enum(SnapshotStatusEnum), nullable=False, index=True)

    publication = relationship('Publication', back_populates='snapshots')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    id_vk: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    screen_name: Mapped[str] = mapped_column(String(255), nullable=True)
    sex: Mapped[SexEnum] = mapped_column(Enum(SexEnum), nullable=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    checked_at: Mapped[Date] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    is_banned: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=True)

    publications = relationship('Publication', back_populates='user')
    activities = relationship('Activity', back_populates='user')

    country = relationship('Country', back_populates='users')
    city = relationship('City', back_populates='users')

    @property
    def is_community(self):
        return self.id_vk < 0

    def __repr__(self):
        return f'User ID {self.id_vk}'


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    id_vk: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users = relationship('User', back_populates='country')
    cities = relationship('City', back_populates='country')

    def __repr__(self):
        return f'Country {self.name} (ID {self.id}, VK_ID {self.id_vk})'


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    id_vk: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'), nullable=True)

    users = relationship('User', back_populates='city')
    country = relationship('Country', back_populates='cities')

    def __repr__(self):
        return f'City {self.name} (ID {self.id}, VK_ID {self.id_vk})'


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    publication_id: Mapped[int] = mapped_column(Integer, ForeignKey('publications.id'), nullable=False)
    type: Mapped[ActivityTypeEnum] = mapped_column(Enum(ActivityTypeEnum), nullable=False)

    user = relationship('User', back_populates='activities')
    publication = relationship('Publication', back_populates='activities')

    def __repr__(self):
        return f'{self.user} did {self.type} for publ {self.publication}'
