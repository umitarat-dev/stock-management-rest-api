from rest_framework.viewsets import ModelViewSet
from .serializers import (
    User, UserSerializer,
)

# ----------------------------------
# UserView -> Full Control for permissions.IsAdminUser
# ----------------------------------
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser] # Default: IsAdminUser settings.py da global olarak belirtildi.


# ----------------------------------
# UserCreateView -> Only CreateUser for permissions.AllowAny
# ----------------------------------
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

class UserCreateView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        from rest_framework import status
        from rest_framework.response import Response
        from rest_framework.authtoken.models import Token
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # <--- User.save() --->
        user = serializer.save()
        
        # <--- Token.create() --->
        token, _ = Token.objects.get_or_create(user=user) # created yerine "_" kullandık çünkü token zaten varsa yeni token oluşturulmaz, var olan token döner.
        data = serializer.data
        data['key'] = token.key
        # </--->
        
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

