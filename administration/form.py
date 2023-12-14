from django import forms
from .models import Coupon
from product.models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['product', 'discount_type', 'discount_value', 'start_date', 'end_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'discount_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'discount_value': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'valid_from', 'valid_to']
        widgets = {
            'code': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control'
            }),
            'discount': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control'
            }),
            'valid_to': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'valid_from': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }