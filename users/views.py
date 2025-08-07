from rest_framework import viewsets

from .models import App_users
from .serializers import UsersSerializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = App_users.objects.all()
    serializer_class = UsersSerializers

    def all_publishers(self):
        pass

    def all_subscribers(self):
        pass