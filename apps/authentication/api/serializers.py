from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'groups']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # If user is superuser, ensure 'Admin' is in groups list for frontend logic
        if instance.is_superuser or instance.is_staff:
            if 'Admin' not in representation['groups']:
                representation['groups'].append('Admin')
        return representation

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if groups_data:
            user.groups.set(groups_data)
        
        return user
