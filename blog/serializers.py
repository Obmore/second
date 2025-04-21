from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    # így tudunk idegen kulccsal dolgozni write módban
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )
    class Meta:
        model = Comment
        # most már include-oljuk a post mezőt is
        fields = ['id', 'post', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'published_at', 'comments']
