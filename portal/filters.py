from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Category, Post
from django.forms import DateInput


class PostListSearch(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())
    date_in = DateFilter(label='По дате:', lookup_expr='lte', widget=DateInput({'type': 'date'}))
    class Meta:
        model = Post
        fields = {
            'title': ['icontains']
        }
