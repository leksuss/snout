from datetime import datetime, timedelta
from typing import Type, Any

from sqlalchemy import select, and_, not_, exists, update
from sqlalchemy.orm import joinedload, aliased


from src.logger import get_logger
from src.db_conn import session as db
from src.vk.models import Publication, User, Activity, PublicationSnapshot, Hashtag, ActivityTypeEnum, SnapshotStatusEnum

logger = get_logger(__name__)


def add_or_get_entity_id(entity_class: Type, entity: dict[str, Any], conditions: list) -> (int, bool):
    query = select(entity_class).where(and_(*conditions))
    existing_entity = db.execute(query).scalars().first()

    if existing_entity:
        return existing_entity.id, False

    new_entity = entity_class(**entity)
    db.add(new_entity)
    db.commit()
    logger.info(f'Added {entity_class.__name__} with ID {new_entity.id}')
    return new_entity.id, True


def get_entities(entity_class: Type, ids: list[int] = None) -> list:
    query = select(entity_class)
    if ids:
        query = query.where(entity_class.id.in_(ids))
    return db.execute(query).scalars().all()

def add_publication(publication: dict) -> int:
    conditions = [
        Publication.id_vk == publication['id_vk']
    ]
    return add_or_get_entity_id(Publication, publication, conditions)

def add_user(user: dict) -> int:
    conditions = [
        User.id_vk == user['id_vk']
    ]
    return add_or_get_entity_id(User, user, conditions)

def add_activity(activity: dict) -> int:
    conditions = [
        Activity.user_id == activity['user_id'],
        Activity.publication_id == activity['publication_id'],
        Activity.type == activity['type'],
    ]
    return add_or_get_entity_id(Activity, activity,conditions)

def add_publication_snapshot(snapshot: dict) -> int:
    one_hour_ago = datetime.now() - timedelta(hours=1)
    conditions = [
        PublicationSnapshot.publication_id == snapshot['publication_id'],
        PublicationSnapshot.status == snapshot['status'],
        # PublicationSnapshot.checked_at >= one_hour_ago,
    ]
    return add_or_get_entity_id(PublicationSnapshot, snapshot, conditions)

def add_hashtag(hashtag: dict) -> int:
    conditions = [
        Hashtag.name == hashtag['name']
    ]
    return add_or_get_entity_id(Hashtag, hashtag, conditions)

def get_hashtags(ids: list | None = None) -> list[Hashtag]:
    return get_entities(Hashtag, ids)

def get_publications(ids: list | None = None) -> list[Publication]:
    return get_entities(Publication, ids)

def update_publication_snapshot_status(publication_id: int, status: SnapshotStatusEnum) -> None:
    query = (
        update(PublicationSnapshot)
        .where(and_(PublicationSnapshot.publication_id == publication_id))
        .values(status=status)
    )
    db.execute(query)
    db.commit()


'''
def get_publications_without_activity(activity_type: ActivityTypeEnum) -> list[Publication]:
    subquery = (
        select(1)
        .where(Activity.publication_id == Publication.id)
        .where(Activity.type == activity_type.value)
    )
    query = (
        select(Publication)
        .options(joinedload(Publication.user))
        .where(not_(exists(subquery)))
    )
    return db.execute(query).scalars().all()
'''

def get_publications_without_activity(activity_type: ActivityTypeEnum) -> list[Publication]:
    activity_subquery = (
        select(1)
        .where(Activity.publication_id == Publication.id)
        .where(Activity.type == activity_type.value)
    )

    LatestSnapshot = aliased(PublicationSnapshot)
    latest_snapshot_subquery = (
        select(PublicationSnapshot.id)
        .where(PublicationSnapshot.publication_id == Publication.id)
        .order_by(PublicationSnapshot.checked_at.desc())
        .limit(1)
        .scalar_subquery()
    )

    query = (
        select(Publication)
        .options(joinedload(Publication.user))
        .join(LatestSnapshot, and_(
            LatestSnapshot.publication_id == Publication.id,
            LatestSnapshot.id == latest_snapshot_subquery
        ))
        .where(and_(
            not_(exists(activity_subquery)),
            LatestSnapshot.status == SnapshotStatusEnum.SUCCESS
        ))
    )

    return db.execute(query).scalars().all()

if __name__ == '__main__':
    pub = get_publications_without_activity(ActivityTypeEnum.LIKE)

    print(len(pub))