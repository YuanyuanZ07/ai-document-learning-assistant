from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'file', 'filename', 'file_type', 'file_size',
            'extracted_text', 'summary', 'status',
            'uploaded_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'filename', 'file_type', 'file_size',
            'extracted_text', 'summary', 'status',
            'uploaded_at', 'updated_at',
        ]


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'file_type', 'file_size', 'status', 'uploaded_at']


class AskQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
