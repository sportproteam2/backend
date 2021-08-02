from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from user.serializers import RegionSerializer, TrainerSerializer, UserSerializer, RoleSerializer, RegistrationSerializer, LoginSerializer
from .models import *
from django_filters.rest_framework import DjangoFilterBackend


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     role_id = self.request.query_params.get('role')
    #     if role_id is not None:
    #         queryset = queryset.filter(role=role_id)
    #     return queryset


class UsersDetail(APIView):
    def get(self, request, pk, format=None):
        users = User.objects.get(pk=pk)
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        users = User.objects.get(pk=pk)
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        users = User.objects.get(pk=pk)
        serializer = serializers.UsersSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserByRoles(generics.RetrieveAPIView):
    model = User
    queryset = User.objects.all()
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        user = User.objects.filter(role = instance.id)
        serializer = UserSerializer(user, many = True)
        return Response(serializer.data)


# class UserViewSet(viewsets.ModelViewSet):
#     # permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['role']


class RegionView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class TrainerView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer