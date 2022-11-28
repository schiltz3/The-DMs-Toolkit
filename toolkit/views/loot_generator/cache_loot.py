from typing import Optional

from django.contrib.auth.models import User

from toolkit.models import Armor, GeneratedLoot, GenericItem, MagicItem, Weapon
from toolkit.utilities.cache import get_cache


def cache_loot(
    user: User,
    loot: GeneratedLoot,
    weapons_output: list[Weapon],
    armors_output: list[Armor],
    generic_items_output: list[GenericItem],
    magic_items_output: list[MagicItem],
):
    """Create and cache a loot object from the loot_generator view

    Args:
        user (User): User to cache the loot on

    """
    loot.save_base()
    loot.Owner = user
    cache = get_cache(user)
    loot_cache = cache.loot
    if loot_cache is not None:
        loot_cache.delete()
    if weapons_output is not None:
        loot.Weapons.set(weapons_output)
    if armors_output is not None:
        loot.Armors.set(armors_output)
    if generic_items_output is not None:
        loot.Generic_Items.set(generic_items_output)
    if magic_items_output is not None:
        loot.Magical_Items.set(magic_items_output)
    loot.save()
    cache.loot = loot
    user.save()


def save_cached_loot(user: User) -> Optional[GeneratedLoot]:
    """Save the cached loot to the database

    Args:
        user (User): User who has the created loot

    Returns:
        Optional[Loot]: Loot if one is cached, else None
    """
    ret = user.cache.loot
    user.cache.loot = None
    user.save()
    return ret


def delete_cached_loot(user: User):
    """Delete cached loot

    Args:
        user (User): User to delete the cache on
    """
    cache = user.cache.loot
    if cache is not None:
        cache.delete()
    user.cache.loot = None
    user.save()
