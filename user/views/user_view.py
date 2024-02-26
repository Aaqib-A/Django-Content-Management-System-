# REST Essentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

# for filter View
from rest_framework import generics
from django_filters import rest_framework as filters
from user.filters import UserFilter

# Extra imports
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password


# Custom Defined Imports
from user.models import User
from user.serializers import UserModelSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permission_class import AdminAllPermission, AuthorAllPermission, AuthorReadPermission
from utils.role_filter_utils import RoleBasedQuery


class UserView(generics.ListAPIView, APIView):
    permission_classes = [IsAuthenticated & 
            ( AdminAllPermission | AuthorReadPermission )
        ]

    serializer_class = UserModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def list(self, request):
        try:
            user = request.user
            utils = RoleBasedQuery(user)
            user_role_query = utils.user_query()

            queryset = User.objects.filter(user_role_query)
            filter_backends = self.filter_queryset(queryset)
            serializer = UserModelSerializer(filter_backends,many=True)
            resp = Response(serializer.data, status=status.HTTP_200_OK)
            return resp
        except Exception as e:
            # log.error("[{user} | GET | UserView Error] Error - {error}".format(user=request.user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            password = data.get('password')
            if not password:
                raise ValidationError("'password' is required")

            with transaction.atomic():
                user_serialized = UserModelSerializer(data=data)
                if user_serialized.is_valid():
                    user_serialized.save()

                    user = User.objects.get(username = user_serialized.data["username"])

                    validate_password(password=password, user=user)
                    user.set_password(password)
                    user.save()

                    resp = user_serialized.data
                else:
                    raise ValidationError(user_serialized.errors)

            return Response(resp, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            # log.error("[{user} | POST | UserView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | UserView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:

            utils = RoleBasedQuery(user)
            user_role_query = utils.user_query()

            user_id = request.GET.get('user_id')
            if not user_id:
                raise ValidationError("'user_id' is required")

            old_user = User.objects.get(user_role_query & Q(user_id = user_id))
            user_serialized = UserModelSerializer(old_user, data=data, partial=True)
            with transaction.atomic():
                if user_serialized.is_valid():
                    user_serialized.save()
                    
                    if "password" in data.keys():
                        validate_password(password=data['password'], user=user)
                        old_user.set_password(data['password'])
                        old_user.save()
                else:
                    raise ValidationError(user_serialized.errors)

            resp = user_serialized.data
            return Response(resp, status=status.HTTP_200_OK)
            
        except User.DoesNotExist as e:
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            # log.error("[{user} | POST | UserView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | UserView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:

            utils = RoleBasedQuery(user)
            user_role_query = utils.user_query()

            user_id = request.GET.get('user_id')
            if not user_id:
                raise ValidationError("'user_id' is required")

            deleted_user = User.objects.get(user_role_query & Q(user_id = user_id))
            deleted_user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except User.DoesNotExist as e:
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            # log.error("[{user} | POST | UserView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | UserView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp
