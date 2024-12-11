import csv
from datetime import datetime

import re

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


from src.logger import app_logger
from src.vk.services import add_publication, add_user, add_publication_snapshot, add_hashtag, get_hashtags
from src.vk.models import PublTypeEnum, SnapshotStatusEnum


class PublicationSchema(BaseModel):
    social_network: str = Field(alias='Социальная сеть')
    publication_type: str = Field(alias='Тип публикации')
    author: str = Field(alias='Автор')
    publication_date: str = Field(alias='Дата публикации')
    publication_link: str = Field(alias='ссылка на публикацию')
    name_or_nickname: str = Field(alias='Имя/Никнейм')
    views: int | str | None = Field(alias='Просмотры')
    hashtags: Optional[List[str]] = Field(default=None, alias='Хэштеги')

    @field_validator('publication_type', mode='before')
    def validete_publication_type(cls, value):
        try:
            return PublTypeEnum(value.upper())
        except ValueError:
            raise ValueError(f'Invalid publication type: {value}')

    @field_validator('hashtags', mode='before')
    def validate_hashtags(cls, value):
        if value:
            return value.split(', ')

    @field_validator('views', mode='before')
    def validate_views(cls, value):
        if value.isnumeric():
            return int(value)

    @property
    def snapshot_status(self):
        if self.views:
            return SnapshotStatusEnum.SUCCESS
        return SnapshotStatusEnum.NOT_FOUND

    @property
    def formatted_date(self):
        return datetime.strptime(self.publication_date, '%Y-%m-%d').date()

    def _get_pair_ids(self):
        types = [type.value.lower() for type in PublTypeEnum]
        matches = re.search(fr'({"|".join(types)})(-?\d+)_(\d+)', self.publication_link)
        if not matches:
            raise ValueError(f'Invalid publication link: {self.publication_link}')
        return matches.group(1, 2, 3)

    @property
    def id_vk_user(self):
        _, id_vk_user, _ = self._get_pair_ids()
        return id_vk_user

    @property
    def id_vk_publication(self):
        _, _, id_vk_publication = self._get_pair_ids()
        return id_vk_publication


def read_csv_to_pydantic_objects(file_path: str) -> List[PublicationSchema]:
    publications = []
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            publication = PublicationSchema(**row)
            publications.append(publication)
    return publications


if __name__ == '__main__':
    file_path = 'links.csv'
    campaign_id = 3
    publications_from_csv = read_csv_to_pydantic_objects(file_path)
    app_logger.info(f'Converting {len(publications_from_csv)} publications from {file_path}')

    for publication_from_csv in publications_from_csv:

        hashtag_ids = []
        for hashtag in publication_from_csv.hashtags:
            hashtag = {
                'name': hashtag,
                'campaign_id': campaign_id,
            }
            hashtag_id, _ = add_hashtag(hashtag)
            hashtag_ids.append(hashtag_id)

        user = {
            'id_vk': publication_from_csv.id_vk_user,
        }
        user_id, _ = add_user(user)

        publication = {
            'id_vk': publication_from_csv.id_vk_publication,
            'user_id': user_id,
            'date_published': publication_from_csv.formatted_date,
            'type': publication_from_csv.publication_type,
            'hashtags': get_hashtags(hashtag_ids),
        }
        publication_id, _ = add_publication(publication)

        snapshot = {
            'publication_id': publication_id,
            'views': publication_from_csv.views,
            'checked_at': datetime(2024, 12, 10, 0, 0, 0),
            'status': publication_from_csv.snapshot_status,
        }
        snapshot_id, _ = add_publication_snapshot(snapshot)

        app_logger.info(f'Added user {user_id} and publ {publication_id} with snapshot {snapshot_id}')
