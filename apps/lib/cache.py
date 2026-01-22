import hashlib
from functools import wraps
from apps.lib.loggers import AppLogger
from django.core.cache import cache
from asgiref.sync import sync_to_async


def cache_result(prefix: str, timeout: int = 3600):
    """
    دکوراتور حرفه‌ای برای کش کردن خروجی سلکتورها.
    prefix: نام اختصاصی برای دسته‌بندی کش (مثل 'product_list')
    timeout: زمان انقضا به ثانیه (پیش‌فرض ۱ ساعت)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_key = f"{prefix}:{func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.md5(raw_key.encode()).hexdigest()
            full_key = f"{prefix}:{cache_key}"

            result = cache.get(full_key)
            if result is not None:
                return result

            try:
                result = func(*args, **kwargs)

                data_to_cache = list(result) if hasattr(result, '__iter__') and not isinstance(result,
                                                                                               (str, dict)) else result

                cache.set(full_key, data_to_cache, timeout)
                return data_to_cache

            except Exception as e:
                AppLogger.log_activity(f"Cache Error in {func.__name__}: {str(e)}", status="ERROR")
                return func(*args, **kwargs)

        return wrapper

    return decorator


async def async_cache_get(key: str):
    return await sync_to_async(cache.get)(key)

async def async_cache_set(key: str, value: any, timeout: int):
    await sync_to_async(cache.set)(key, value, timeout)