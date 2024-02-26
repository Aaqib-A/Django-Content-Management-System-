import django_filters
from django.db.models import Q
from content.models import Content

class ContentFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_content_search', label='Search')
    
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    body = django_filters.CharFilter(field_name='body', lookup_expr='icontains')
    summary = django_filters.CharFilter(field_name='summary', lookup_expr='icontains')
    categories = django_filters.CharFilter(field_name='categories', lookup_expr='icontains')
    
    class Meta:
        model = Content
        fields = {
            'content_id': ['exact'],
        }
    
    def custom_content_search(self, queryset, name, value):
        return queryset.filter(
        Q(title__icontains=value) | Q(body__icontains=value) | Q(summary__icontains=value)
    )
