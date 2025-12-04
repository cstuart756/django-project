from django import forms
from .models import Category, Review

class ProductSearchForm(forms.Form):
    query = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    min_rating = forms.IntegerField(required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
