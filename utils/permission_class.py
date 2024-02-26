from rest_framework.permissions import BasePermission

from utils.constants import ROLES

class AdminAllPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.ADMIN.value:
            return True
        else:
            return False
        
class AuthorAllPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.AUTHOR.value:
            return True
        else:
            return False

# NOTE: Just for demo purpose
class AuthorReadPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == ROLES.AUTHOR.value and (request.method=='GET'):
            return True
        else:
            return False