from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dinosaur, Comment
User = get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class DinosaurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dinosaur
        fields = '__all__'

class PopulatedCommentSerializer(CommentSerializer):
    owner = UserSerializer()

class PopulatedDinosaurSerializer(DinosaurSerializer):
    comments = PopulatedCommentSerializer(many=True)
    