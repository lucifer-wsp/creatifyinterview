import json
from functools import wraps

from django.http import JsonResponse


def require_http_methods(request_method_list):
    """自定义装饰器限制 HTTP 方法"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            if request.method not in request_method_list:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def add_data_property(func):
    """装饰器：为 request 添加 data 属性"""
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        # 为 request 添加 data 属性
        if hasattr(request, 'body') and not hasattr(request, 'data'):
            try:
                request.data = json.loads(request.body) if request.body else {}
            except json.JSONDecodeError:
                request.data = {}
        return await func(request, *args, **kwargs)
    return wrapper
