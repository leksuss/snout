import json
import re
import time
from itertools import batched

import httpx
from bs4 import BeautifulSoup

from src.logger import get_logger
from src.vk.models import PublTypeEnum
from src.vk.schemas import (
    LikesFirstResponseSchema,
    LikesRestResponseSchema,
    AccessResponseSchema,
    UserSchema,
)
from src.vk.exceptions import AccessDeniedException, NotFoundException


logger = get_logger(__name__)


def parse_id_vk_users(chunk_data):
    html1 = LikesFirstResponseSchema(**chunk_data).html_content or ''
    html2 = LikesRestResponseSchema(**chunk_data).html_content or ''
    soup = BeautifulSoup(html1 + html2, 'html.parser')
    user_rows = soup.find_all('div', class_='fans_fan_row')
    data_ids = set(int(div.get('data-id')) for div in user_rows)
    return data_ids or None


def fetch_chunk_likes(publ_uri: str, offset: int = 0):
    url = 'https://vk.com/wkview.php?act=show'
    payload = {
        'al': '1',
        'offset': str(offset),
        'w': f'likes/{publ_uri}',
    }
    with httpx.Client() as client:
        response = client.post(url, data=payload)
        response.raise_for_status()

    json_str = re.sub(r'^<!--\s*|\s*-->$', '', response.text.strip())

    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        logger.error(f'Error parsing JSON: {e}. Payload: {payload}. Data: {json_str[:100]} ... (truncated)')


def fetch_users_from_likes(publ_type: PublTypeEnum, id_vk_user: int, id_vk_publication: int) -> set[int]:
    publ_uri = f'{publ_type.value.lower()}{str(id_vk_user)}_{str(id_vk_publication)}'
    offset = 0
    count_chunks = 0
    users = set()
    while True:
        logger.info(f'Fetching likes chunk {count_chunks} for {publ_uri}')
        try:
            chunk_data = fetch_chunk_likes(publ_uri, offset)

            if AccessResponseSchema(**chunk_data).is_access_denied:
                raise AccessDeniedException

            if AccessResponseSchema(**chunk_data).is_not_found:
                raise NotFoundException

            if not chunk_data:
                logger.info(f'No more chunks for {publ_uri}')
                break

            chunk_users = parse_id_vk_users(chunk_data)
            if not chunk_users:
                logger.info(f'No more likes for {publ_uri}')
                break

            users.update(chunk_users)
            offset += 60

        except AccessDeniedException:
            logger.info(f'Access denied for {publ_uri}')
            raise
        except NotFoundException:
            logger.info(f'Not found {publ_uri}')
            raise
        except Exception as e:
            logger.error(f'Error fetching likes chunk: {e}. Payload: {publ_uri}, offset: {offset}')
            break

        count_chunks += 1
        time.sleep(1)
    return users


def fetch_users_chunk(api_key: str, user_ids:tuple[int, ...]) -> list[UserSchema] | None:
    VK_API_URL = 'https://api.vk.com/method/users.get'
    VK_API_VERSION = 5.199

    fields = (
        'sex',
        'screen_name',
        'first_name',
        'last_name',
        'bdate',
        'city',
    )
    payload = {
        'user_ids': ','.join(map(str, user_ids)),
        'fields': ','.join(fields),
        'v': VK_API_VERSION,
        'access_token': api_key
    }
    with httpx.Client() as client:
        response = client.post(VK_API_URL, data=payload)
        response.raise_for_status()

    try:
        response_json = response.json()
    except json.JSONDecodeError as e:
        logger.error(f'Error parsing JSON: {e}. Payload: {payload}. Data: {response.text[:100]} ... (truncated)')
        return None

    if 'error' in response_json or 'response' not in response_json:
        logger.error(f'VK API error for payload: {payload}. Data: {response_json}')
        return None

    return [UserSchema(**user) for user in response_json['response']]


def fetch_users(api_key, user_ids:tuple[int, ...]) -> list[UserSchema] | None:
    CHUNK_SIZE = 1000  # max count of users per request, VK limit
    count_chunks = 0
    users = []
    for user_ids_chunk in batched(user_ids, CHUNK_SIZE):
        logger.info(f'Fetching users, batch {count_chunks}')
        try:
            users_chunk = fetch_users_chunk(api_key, user_ids_chunk)
            if users_chunk:
                users.extend(users_chunk)
        except Exception as e:
            logger.error(f'Error fetching users: {e}')
            break
        count_chunks += 1
        time.sleep(5)
    return users


if __name__ == '__main__':
    # print(fetch_chunk_likes("clip-222681453_456241259", offset=120))
    # users = fetch_users_from_likes(PublTypeEnum.WALL, -220568323, 893)
    from src.config import settings
    users_ids = (10000, 10001, 10002, 1901501, 343379968)
    users = fetch_users(settings.VK_PERMANENT_API_KEY, users_ids)
    print(users)


    data = '''
    <div class="fans_fan_row inl_bl" id="fans_fan_row181149506" data-id="181149506">
      <div class="fans_fanph_wrap " >
        <a class="fans_fan_ph " href="/elisasue">
          <img class="fans_fan_img" src="https://sun6-22.userapi.com/s/v1/ig2/jglFPLWo1nHfpWgTtpSf63vmwpA_hV2U3jI04BdXcpSPZMnyUNMc2fyuZX-RHnpKIzaKtn_5qDgWCgcUAl5OxYDj.jpg?quality=95&crop=5,42,1414,1414&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1080x1080,1280x1280&ava=1&cs=100x100" alt="Elizaveta Egorova" />
        </a>
        
      </div>
      <div class="fans_fan_name"><a class="fans_fan_lnk" href="/elisasue">Elizaveta Egorova</a></div>
    </div><div class="fans_fan_row inl_bl" id="fans_fan_row348367640" data-id="348367640">
      <div class="fans_fanph_wrap " >
        <a class="fans_fan_ph " href="/zaebalovco1703">
          <img class="fans_fan_img" src="https://sun6-21.userapi.com/s/v1/ig2/XVIc9n8kf3-3bw4Ej4DCyhC2BjSCyXpLRrmgwkhdFHHrOHHL77lt5uGl0pmg7EYE7XLRRHSbICjDzNTdDYrpZjs-.jpg?quality=95&crop=291,179,679,679&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640&ava=1&cs=100x100" alt="Tania Gaiko" />
        </a>
        
      </div>
      <div class="fans_fan_name"><a class="fans_fan_lnk" href="/zaebalovco1703">Tania Gaiko</a></div>
    </div><div class="fans_fan_row inl_bl" id="fans_fan_row240784623" data-id="240784623">
      <div class="fans_fanph_wrap " >
        <a class="fans_fan_ph " href="/id240784623">
          <img class="fans_fan_img" src="https://sun6-21.userapi.com/s/v1/ig2/c9Io1ndRFyhC327bDOR-6MedXOtY0Q2RJXnVgM6QEBl-A6fBUiXziqWz6gs2OSEyZq7PjtEz_95zAuhjhh71OiJw.jpg?quality=95&crop=670,0,957,957&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720&ava=1&cs=100x100" alt="Olga Ivanova" />
        </a>
        
      </div>
      <div class="fans_fan_name"><a class="fans_fan_lnk" href="/id240784623">Olga Ivanova</a></div>
    </div>
    '''

    # print(parse_id_vk_users(data))