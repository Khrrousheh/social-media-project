from rest_framework import serializers

from .models import App_users

class UsersSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
         model = App_users
         fields = ['username', 'is_publisher', 'email', 'is_active']
