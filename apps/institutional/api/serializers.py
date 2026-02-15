from rest_framework import serializers
from apps.institutional.models import UploadedDocument
from django.contrib.auth.models import User

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['title', 'file']

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinimalSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedDocument
        fields = ['id', 'title', 'file_url', 'uploaded_at', 'status', 'uploaded_by']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

class DocumentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['status']
    
    def validate_status(self, value):
        if value not in ['APPROVED', 'REJECTED']:
            raise serializers.ValidationError("Status must be APPROVED or REJECTED")
        return value
