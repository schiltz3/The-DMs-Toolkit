from django.contrib.auth.models import User

from toolkit.models import Cache


def get_cache(user: User) -> Cache:
    """Gets the user cache and creates a new one if it does not exist

    Args:
        user (User): user to get cache for

    Returns:
        Cache: Cache model
    """
    if not hasattr(user, "cache"):
        user.cache = Cache()
    return user.cache
