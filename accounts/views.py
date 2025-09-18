import asyncio
import logging
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from asgiref.sync import sync_to_async

from utils.http_utils import require_http_methods, add_data_property
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


@csrf_exempt
@add_data_property
@require_http_methods(['POST'])
@permission_classes([AllowAny])
async def signup(request):
    """用户注册"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    # 异步验证序列化器
    is_valid = await sync_to_async(serializer.is_valid)()
    
    if is_valid:
        user = await sync_to_async(serializer.save)()

        return JsonResponse({
            'id': user.id,
            'email': user.email
        }, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@add_data_property
@require_http_methods(['POST'])
@permission_classes([AllowAny])
async def signin(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    
    # 异步验证序列化器
    is_valid = await sync_to_async(serializer.is_valid)()
    
    if is_valid:
        user = serializer.validated_data['user']
        _ = await update_last_login(user)
        refresh = await sync_to_async(RefreshToken.for_user)(user)

        return JsonResponse({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=200)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@require_http_methods(['GET'])
@permission_classes([IsAuthenticated])
async def me(request):
    """获取当前用户信息"""
    # 检查用户是否已认证
    if not request.user or not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data, status=200)


async def update_last_login(user):
    """异步更新最后登录时间"""
    await asyncio.to_thread(
        lambda: User.objects.filter(id=user.id).update(last_login=timezone.now())
    )
