from sportpro_app.models import Federation, Sport
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Admin, Editor, Judge, Region, Trainer, User, Role
from rest_framework.authtoken.models import Token
from firebase_admin import auth
# from sportpro_app.serializers import SportSerializer


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
        fields = ['name', 'surname', 'middlename', 'region', 'phone', 'sport', 'role', 'password', 'token']

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


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name']



class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    region = RegionSerializer(many=False)
    role = RoleSerializer(many=False)
    sport = serializers.PrimaryKeyRelatedField(queryset=Sport.objects.all())
    

    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'middlename', 'phone', 'role', 'region', 'organization', 'sport', 'password', 'document')
        depth = 1
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        return instance


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