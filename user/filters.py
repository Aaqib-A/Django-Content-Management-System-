import django_filters
from django.db.models import Q
from user.models import User

class UserFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_user_search', label='Search')
    
    first_name= django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name= django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    class Meta:
        model = User
        fields = {
            'user_id': ['exact'],
            'role': ['exact'],
        }
    
    def custom_user_search(self, queryset, name, value):
        return queryset.filter(
        Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value)
    )