from sportpro_app.models import Federation
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Admin, Editor, Judge, Trainer, User, Role
from rest_framework.authtoken.models import Token
from firebase_admin import auth


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['name', 'surname', 'phone', 'username', 'role', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255, write_only=True)
    # id_token = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # id_token = data.get('id_token')
        phone = data.get('phone', None)

        # decoded_token = auth.verify_id_token(id_token)
        # uid = decoded_token['uid']
        # print(uid)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "A user with this phone number does not exist")

        token, _ = Token.objects.get_or_create(user=user)
        return {
            'token': token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'surname', 'phone', 'role', 'password', 'age', 'is_active', 'is_staff', 'created_at', 'updated_at')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        return instance

class RoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_name")
    name = serializers.ReadOnlyField(source='get_name_display')

    class Meta:
        model = Role
        fields = ['id', 'name']

    def get_name(self):
        return self.get_name_display


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    federation = serializers.PrimaryKeyRelatedField(queryset=Federation.objects.all())

    class Meta:
        model = Admin
        fields = ['id', 'user', 'federation']


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Trainer
        fields = ['id', 'user', 'is_approved']


class EditorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Editor
        fields = ['id', 'user']


class JudgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Judge
        fields = ['id', 'user', 'experience']