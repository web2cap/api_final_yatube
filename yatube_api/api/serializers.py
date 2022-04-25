from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post, User


class FollowSerializer(serializers.ModelSerializer):
    # achievement_name = serializers.CharField(source='name')
    following = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        following = validated_data["following"]
        user = validated_data["user"]

        if user == following:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(following=following, user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(**validated_data)
        return follow

    class Meta:
        model = Follow
        fields = ("user", "following")


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        ref_name = "ReadOnlyUsers"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")
