# -*- coding: utf-8 -*-
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationMiddleware:
    """JWT 认证中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        # 检查 Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                # 同步验证 JWT token
                validated_token = self.jwt_auth.get_validated_token(token)
                user = self.jwt_auth.get_user(validated_token)
                
                # 将认证的用户注入到 request 中
                request.user = user

            except Exception:
                # 认证失败，保持 request.user 为 AnonymousUser
                pass
        
        response = self.get_response(request)
        return response
