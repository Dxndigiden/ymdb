from django.contrib.auth import get_user_model
from rest_framework import (viewsets, filters, permissions)
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer
from api.permissions import IsAdmin


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'delete', 'patch')

    @action(
        detail=False,
        url_path='me',
        methods=('get', 'patch'),
        permission_classes=(permissions.IsAuthenticated,),)
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data)
