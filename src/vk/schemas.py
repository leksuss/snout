from enum import Enum
from pydantic import BaseModel
from typing import Union, Optional

from src.logger import get_logger


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


if __name__ == '__main__':
    text = {'payload': ['a;lfjaldsjf']}
    print(AccessResponseSchema(**text).is_not_found)
