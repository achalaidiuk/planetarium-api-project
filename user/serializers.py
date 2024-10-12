from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "username", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password"),
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        username = validated_data.pop("username")
        user = get_user_model().objects.create_user(
            email=validated_data.get("email"),
            username=username,
            password=password,
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
