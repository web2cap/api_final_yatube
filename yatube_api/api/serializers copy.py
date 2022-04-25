from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post, User


class FollowSerializer(serializers.ModelSerializer):
    # following = serializers.StringRelatedField(read_only=True)
    # user = serializers.StringRelatedField(read_only=True)

    following = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    def validate(self, data):
        print("here")
        for v in data:
            print(f"{v}")
        if "following" in data:
            if data["following"] == data["user"]:
                raise serializers.ValidationError(
                    "Сам на себя не подпишешься!"
                )
            else:
                return data
        else:
            raise serializers.ValidationError("Нет объекта для подписки")

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
