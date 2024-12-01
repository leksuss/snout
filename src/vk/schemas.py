from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Union, Optional, Literal

from src.logger import get_logger

from src.vk.models import SexEnum


logger = get_logger(__name__)


class VKTextResponseEnum(Enum):
    ACCESS_DENIED = 'acceso denegado'
    NOT_FOUND = 'gina no encontrada'


class LikesPreloadSchema(BaseModel):
    preload: Optional[list[Union[str, int, bool]] | bool] = None

    @property
    def html_content(self) -> Optional[str]:
        if self.preload and isinstance(self.preload[0], str):
            return self.preload[0]


class LikesFirstResponseSchema(BaseModel):
    payload: list[Union[int, list, dict]]

    @property
    def html_content(self) -> str:
        results = ''

        try:
            preload_data = LikesPreloadSchema(**self.payload[1][2])
            results += preload_data.html_content
        except (IndexError, KeyError, TypeError):
            pass

        try:
            if isinstance(self.payload[1][1], str):
                results += self.payload[1][1]
        except IndexError:
            pass

        return results


class LikesRestResponseSchema(BaseModel):
    payload: list

    @property
    def html_content(self) -> list[str]:
        try:
            if isinstance(self.payload[1][0], str):
                return self.payload[1][0]
        except IndexError:
            pass


class AccessResponseSchema(BaseModel):
    payload: list

    @property
    def is_access_denied(self) -> bool:
        try:
            if VKTextResponseEnum.ACCESS_DENIED.value in self.payload[1][0].lower():
                return True
        except (TypeError, IndexError, AttributeError):
            pass
        return False

    @property
    def is_not_found(self) -> bool:
        try:
            if VKTextResponseEnum.NOT_FOUND.value in self.payload[1][0].lower():
                return True
        except (TypeError, IndexError, AttributeError):
            pass
        return False


class CitySchema(BaseModel):
    id: int
    title: str


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    screen_name: str
    sex: Literal[0, 1, 2]
    is_closed: bool
    bdate: str | None = None
    deactivated: Literal['deleted', 'banned'] | None = None
    city: CitySchema | None = None


    @property
    def birthday(self):
        try:
            return datetime.strptime(self.bdate, '%d.%m.%Y').date()
        except (ValueError, TypeError):
            pass
        return None

    @property
    def is_deleted(self):
        if self.deactivated == 'deleted':
            return True
        return False

    @property
    def is_banned(self):
        if self.deactivated == 'banned':
            return True
        return False

    @property
    def get_sex(self):
        sex_mapping = {
            1: SexEnum.FEMALE,
            2: SexEnum.MALE,
            0: SexEnum.UNKNOWN,
        }
        return sex_mapping[self.sex]


if __name__ == '__main__':
    users_json = '''
    {
    "response": [
        {
            "id": 10000,
            "bdate": "14.6",
            "city": {
                "id": 2,
                "title": "Санкт-Петербург"
            },
            "sex": 2,
            "screen_name": "martinz",
            "first_name": "Martinz",
            "last_name": "Smitt",
            "can_access_closed": false,
            "is_closed": true
        },
        {
            "id": 10001,
            "bdate": "18.7",
            "city": {
                "id": 2,
                "title": "Санкт-Петербург"
            },
            "sex": 1,
            "screen_name": "id10001",
            "first_name": "Кристина",
            "last_name": "Киселева",
            "can_access_closed": false,
            "is_closed": true
        },
        {
            "id": 10002,
            "bdate": "3.9",
            "sex": 1,
            "screen_name": "mariawaf",
            "deactivated": "banned",
            "first_name": "Юля",
            "last_name": "Свиридова",
            "can_access_closed": false,
            "is_closed": true
        },
        {
            "id": 1901501,
            "sex": 0,
            "screen_name": "id1901501",
            "deactivated": "deleted",
            "first_name": "DELETED",
            "last_name": "",
            "can_access_closed": true,
            "is_closed": false
        },
        {
            "id": 343379968,
            "bdate": "25.10.1970",
            "city": {
                "id": 110,
                "title": "Пермь"
            },
            "sex": 2,
            "screen_name": "bakharev70",
            "first_name": "Андрей",
            "last_name": "Бахарев",
            "can_access_closed": true,
            "is_closed": false
        }
    ]
    }
    '''
    import json
    users = json.loads(users_json)
    print(UsersSchema(**users))
