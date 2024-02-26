# REST Essentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

# for filter View
from rest_framework import generics
from django_filters import rest_framework as filters
from content.filters import ContentFilter

# Extra imports
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password


# Custom Defined Imports
from content.models import Content
from content.serializers import ContentModelSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permission_class import AdminAllPermission, AuthorAllPermission, AuthorReadPermission
from utils.role_filter_utils import RoleBasedQuery
from utils.input_helper import RequestInputHelper


class ContentView(generics.ListAPIView, APIView):
    permission_classes = [IsAuthenticated & 
            ( AdminAllPermission | AuthorAllPermission )
        ]

    serializer_class = ContentModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContentFilter

    def list(self, request):
        try:
            user = request.user
            utils = RoleBasedQuery(user)
            content_role_query = utils.content_query()

            queryset = Content.objects.filter(content_role_query)
            filter_backends = self.filter_queryset(queryset)
            serializer = ContentModelSerializer(filter_backends,many=True)
            resp = Response(serializer.data, status=status.HTTP_200_OK)
            return resp
        except Exception as e:
            # log.error("[{user} | GET | ContentView Error] Error - {error}".format(user=request.user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            input_helper.created_modified_by_post()
            input_helper.content_post_author()
            # input_helper.replace_string_to_array("categories")
            # input_helper.replace_array_to_str("categories")
            input_helper.content_categories_helper()
            data = input_helper.return_data()

            content_serialized = ContentModelSerializer(data=data)
            if content_serialized.is_valid():
                content_serialized.save()
                resp = content_serialized.data
            else:
                raise ValidationError(content_serialized.errors)

            return Response(resp, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            # log.error("[{user} | POST | ContentView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | ContentView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        try:

            utils = RoleBasedQuery(user)
            content_role_query = utils.content_query()

            content_id = request.GET.get('content_id')
            if not content_id:
                raise ValidationError("'content_id' is required")
            
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            input_helper.created_modified_by_patch()
            print("Yo! 3")
            input_helper.content_patch_author()
            print("Yo!")
            input_helper.content_categories_helper()
            print("Yo! 2")
            data = input_helper.return_data()

            old_content = Content.objects.get(content_role_query & Q(content_id = content_id))
            content_serialized = ContentModelSerializer(old_content, data=data, partial=True)
            with transaction.atomic():
                if content_serialized.is_valid():
                    content_serialized.save()
                else:
                    raise ValidationError(content_serialized.errors)

            resp = content_serialized.data
            return Response(resp, status=status.HTTP_200_OK)
            
        except Content.DoesNotExist as e:
            # log.error("[{user} | POST | ContentView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            # log.error("[{user} | POST | ContentView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | ContentView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:

            utils = RoleBasedQuery(user)
            content_role_query = utils.content_query()

            content_id = request.GET.get('content_id')
            if not content_id:
                raise ValidationError("'content_id' is required")

            deleted_content = Content.objects.get(content_role_query & Q(content_id = content_id))
            deleted_content.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Content.DoesNotExist as e:
            # log.error("[{user} | POST | ContentView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            # log.error("[{user} | POST | ContentView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            # log.exception("[{user} | POST | ContentView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp
