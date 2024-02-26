from django_filters import FilterSet, ModelChoiceFilter
from .models import Ad

class AdFilter(FilterSet):
    ad = ModelChoiceFilter(
        empty_label='все объявления',
        field_name='advert',
        queryset=Ad.objects.all(),
        label='Поиск по объявлению',
        lookup_expr='exact',
    )
class Meta:
    model = Ad
    fields = fields = ['advert',]



