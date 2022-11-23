from typing import Optional

from django.contrib.auth.models import User

from toolkit.models import Armor, GeneratedEncounter, Monster
from toolkit.utilities.cache import get_cache


def cache_encounter(
    user: User,
    encounter: GeneratedEncounter,
    monster_output: list[Monster],
):
    """Create and cache an encounter object from the encounter_generator view

    Args:
        user (User): User to cache the encounter on

    """
    encounter.save_base()
    encounter.Owner = user
    cache = get_cache(user)
    encounter_cache = cache.encounter
    if encounter_cache is not None:
        encounter_cache.delete()
    if monster_output is not None:
        encounter.Monsters.set(monster_output)
    encounter.save()
    cache.encounter = encounter
    user.save()


def save_cached_encounter(user: User) -> Optional[GeneratedEncounter]:
    """Save the cached encounter to the database

    Args:
        user (User): User who has the created encounter

    Returns:
        Optional[Encounter]: Encounter if one is cached, else None
    """
    ret = user.cache.encounter
    user.cache.encounter = None
    user.save()
    return ret


def delete_cached_encounter(user: User):
    """Delete cached encounter

    Args:
        user (User): User to delete the cache on
    """
    cache = user.cache.encounter
    if cache is not None:
        cache.delete()
    user.cache.encounter = None
    user.save()
