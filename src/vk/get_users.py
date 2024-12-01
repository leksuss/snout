from src.vk.services import get_unprocessed_user_ids, update_user, add_city
from src.vk.scraper import fetch_users

from src.config import settings

from src.logger import app_logger as logger

user_ids = get_unprocessed_user_ids()
logger.info(f'Found {len(user_ids)} users to update')

logger.info('Fetching users from VK...')
users = fetch_users(settings.VK_PERMANENT_API_KEY, user_ids)
logger.info(f'Fetched {len(users)} users from VK')

for user in users:
    city_id = None
    if user.city:
        city_id, _ = add_city({
            'id_vk': user.city.id,
            'name': user.city.title,
        })

    user_id = update_user({
        'id_vk': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'screen_name': user.screen_name,
        'sex': user.get_sex,
        'is_closed': user.is_closed,
        'birthday': user.birthday,
        'is_banned': user.is_banned,
        'is_deleted': user.is_deleted,
        'city_id': city_id,
    })
    logger.info(f'Updated user with ID {user_id}')


'''

Пользователь, где все нужные поля заполнены:
https://vk.com/id343379968
    
Пользователь удален:
https://vk.com/id1901501

Пользователь без города и без screen_name:
https://vk.com/id763097090

Пользователь не из России:
https://vk.com/evgenia.nekrasova

'''