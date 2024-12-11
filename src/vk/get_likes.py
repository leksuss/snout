import time

from src.logger import app_logger as logger
from src.vk.scraper import fetch_users_from_likes
from src.vk.models import ActivityTypeEnum, SnapshotStatusEnum
from src.vk.services import (
    add_activity,
    add_user,
    get_publications_without_activity,
    update_publication_snapshot_status,
)
from src.vk.exceptions import AccessDeniedException, NotFoundException


def process_publication(publication):
    liked_user_ids = []
    try:
        liked_user_ids = fetch_users_from_likes(publication.type, publication.user.id_vk, publication.id_vk)
    except AccessDeniedException:
        update_publication_snapshot_status(publication.id, SnapshotStatusEnum.ACCESS_DENIED)
    except NotFoundException:
        update_publication_snapshot_status(publication.id, SnapshotStatusEnum.NOT_FOUND)

    logger.info(f'Found {len(liked_user_ids)} likes')

    count_users_created = 0
    count_activities_created = 0
    for liked_user_id in liked_user_ids:
        user_id, user_is_created = add_user({
            'id_vk': liked_user_id
        })
        _, activity_is_created = add_activity({
            'user_id': user_id,
            'publication_id': publication.id,
            'type': ActivityTypeEnum.LIKE
        })
        if user_is_created:
            count_users_created += 1
        if activity_is_created:
            count_activities_created += 1

    logger.info(f'Created {count_users_created} users and {count_activities_created} activities')

def main():
    CAMPAIGN_ID = 3
    publications = get_publications_without_activity(ActivityTypeEnum.LIKE, CAMPAIGN_ID)
    count_publications = len(publications)
    logger.info(f'Found {len(publications)} publications without likes')

    for publication in publications:
        logger.info(f'Processing publication {publication}')
        process_publication(publication)
        logger.info(f'Finished processing publication {publication}')
        count_publications -= 1
        logger.info(f'{count_publications} left to process')
        time.sleep(3)

if __name__ == "__main__":
    main()