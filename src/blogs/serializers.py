from django.utils import timezone
from rest_framework import serializers

from blogs.models import Blog, Post


class BlogsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ("id", "name", "description", "owner")

class PostsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "attachment", "abstract", "date_pub")

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "abstract", "body", "categories", "attachment", "blog", "date_pub")

    def validate_blog(self, value):
        user = self.context.get("request").user
        view = self.context.get("view")

#       El blog debe pertenecer al usuario que hace la modificación
#       No se debe validar en el caso de un superusuario haciendo un update (por si quiere hacer no público el post de otro usuario)
        if self.context.get("request").user.id == value.owner.id or (view.action == "update" and user.is_superuser):
            return value

        raise serializers.ValidationError("Informed blog does not belong to the user")
