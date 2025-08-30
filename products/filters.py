import django_filters
from .models import Product

class ProductsFilters(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    keyword = django_filters.filters.CharFilter(field_name='name' , lookup_expr='icontains')
    minprice = django_filters.filters.NumberFilter(field_name='price' or 0 , lookup_expr='gte') # اكبر او بساوى 
    maxprice = django_filters.filters.NumberFilter(field_name='price' or 100000 , lookup_expr='lte') # اقل او بساوى 
    
    class Meta: 
        model = Product
        fields = ['category', 'brand', 'name' , 'keyword' , 'minprice' , 'maxprice']


